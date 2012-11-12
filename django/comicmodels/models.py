import os
import re
import pdb

from django import forms
from django.conf import settings
from django.contrib.auth.models import Group,User,Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Max
from django.db.models import Q
from django.utils.safestring import mark_safe

from guardian.shortcuts import assign,remove_perm

from dataproviders import FileSystemDataProvider



def giveFileUploadDestinationPath(uploadmodel,filename):
    """ Where should this file go relative to MEDIA_ROOT? """
    
    path = os.path.join(uploadmodel.comicsite.short_name,"uploads",filename)    
    return path


def get_anonymous_user():
    """Anymous user is the default user for non logged in users. I is also the only member of group
      'everyone' for which permissions can be set """
    return User.objects.get(username = "anonymousUser")


class ComicSiteManager(models.Manager):
    """ adds some tabel level functions for getting ComicSites from db. """ 
    
    def non_hidden(self):
        """ like all(), but only return ComicSites for which hidden=false"""
        return self.filter(hidden=False)
    

class ComicSite(models.Model):
    """ A collection of HTML pages using a certain skin. Pages can be browsed and edited."""
    
    short_name = models.CharField(max_length = 50, default="", help_text = "short name used in url, specific css, files etc. No spaces allowed")
    skin = models.CharField(max_length = 225, blank=True, help_text = "additional css to use for this comic site. Not required")    
    description = models.CharField(max_length = 1024, default="", blank=True,help_text = "Short summary of this project, max 1024 characters.")
    logo = models.URLField(help_text = "URL of a 200x200 image to use as logo for this comicsite in overviews",default="http://www.grand-challenge.org/images/a/a7/Grey.png")
    hidden = models.BooleanField(default=False, help_text = "Do not display this Project in any public overview")
    
    objects = ComicSiteManager()
    
    def __unicode__(self):
        """ string representation for this object"""
        return self.short_name
    
    def clean(self):
        """ clean method is called automatically for each save in admin"""
        pass
        #TODO check whether short name is really clean and short!        
            
    def admin_group_name(self):
        """ returns the name of the admin group which should have all rights to this ComicSite instance"""
        return self.short_name+"_admins"
    
    def participants_group_name(self):
        """ returns the name of the participants group, which should have some rights to this ComicSite instance"""
        return self.short_name+"_participants"
    
    def get_relevant_perm_groups(self):
        """ Return all auth groups which are directly relevant for this ComicSite. 
            This method is used for showin permissions for these groups, even if none
            are defined """
                
        groups = Group.objects.filter(Q(name="everyone") | Q(name=self.admin_group_name()) | Q(name=self.participants_group_name()))
        return groups
    
    

class ComicSiteModel(models.Model):
    """An object which can be shown or used in the comicsite framework. This base class should handle common functions
     such as authorization.
    """
    #user = models.ManyToManyField()
    title = models.CharField(max_length=64, blank=True)
    comicsite = models.ForeignKey(ComicSite, help_text = "To which comicsite does this object belong? Used to determine permissions")
    
    ALL = 'ALL'
    REGISTERED_ONLY = 'REG'
    ADMIN_ONLY = 'ADM'
    
    PERMISSIONS_CHOICES = (
        (ALL, 'All'),
        (REGISTERED_ONLY, 'Registered users only'),
        (ADMIN_ONLY, 'Administrators only')        
    )
    permission_lvl = models.CharField(max_length=3,
                                      choices=PERMISSIONS_CHOICES,
                                      default=ALL)
    
    # = models.CharField(max_length=64, blank=True)
        
    
    def __unicode__(self):
       """ string representation for this object"""
       return self.title
   
    def can_be_viewed_by(self,user):
        """ boolean, is user allowed to view this? """
        
        # check whether everyone is allowed to view this. Anymous user is the only member of group
        # 'everyone' for which permissions can be set
        anonymousUser = get_anonymous_user()
        #pdb.set_trace()        
        
        if anonymousUser.has_perm("view_ComicSiteModel",self):
            return True
        else:
            # if not everyone has access, check whether given user has permissions
            return user.has_perm("view_ComicSiteModel",self)
        
    
    def setpermissions(self, lvl):
        """ Give the right groups permissions to this object 
            object needs to be saved befor setting perms"""
        
        admingroup = Group.objects.get(name=self.comicsite.admin_group_name())
        participantsgroup = Group.objects.get(name=self.comicsite.short_name+"_participants")
        everyonegroup = Group.objects.get(name="everyone")
        self.persist_if_needed()
        if lvl == self.ALL:
            #pdb.set_trace()
            assign("view_ComicSiteModel",admingroup,self)
            assign("view_ComicSiteModel",participantsgroup,self)
            assign("view_ComicSiteModel",everyonegroup,self)                    
        elif lvl == self.REGISTERED_ONLY:
            
            assign("view_ComicSiteModel",admingroup,self)
            assign("view_ComicSiteModel",participantsgroup,self)
            remove_perm("view_ComicSiteModel",everyonegroup,self)                    
        elif lvl == self.ADMIN_ONLY:
            
            assign("view_ComicSiteModel",admingroup,self)
            remove_perm("view_ComicSiteModel",participantsgroup,self)
            remove_perm("view_ComicSiteModel",everyonegroup,self)                    
        else:
            raise ValueError("Unknown permissions level '"+ lvl +"'. I don't know which groups to give permissions to this object")
        
    def persist_if_needed(self):
        """ setting permissions needs a persisted object. This method makes sure."""
        if not self.id:
            super(ComicSiteModel,self).save()

    def save(self):
        """ split save into common base part for all ComicSiteModels and default which can be overwritten """        
        
        if self.id:
            firstcreation = False
        else:
            firstcreation = True
            
        #common save functionality for all models
        self._save_base()                
        self.save_default(firstcreation)
        super(ComicSiteModel,self).save()
    
    
    def _save_base(self):
        """ common save functionality for all models """                
        #make sure this object gets the permissions set in the form            
        self.setpermissions(self.permission_lvl)        
        
        
    def save_default(self,firstcreation):
        """ overwrite this in child methods for custom save functionality 
            object is saved after this method so no explicit save needed"""                
        pass

                
    class Meta:
       abstract = True
       permissions = (("view_ComicSiteModel", "Can view Comic Site Model"),)


class Page(ComicSiteModel):
    """ A single editable page containing html and maybe special output plugins """
    
    order = models.IntegerField(editable=False, default=1, help_text = "Determines order in which page appear in site menu")        
    display_title = models.CharField(max_length = 255, default="", blank=True, help_text = "On pages and in menu items, use this text. Spaces and special chars allowed here. Optional field. If emtpy, title is used")
    hidden = models.BooleanField(default=False, help_text = "Do not display this page in site menu")
    html = models.TextField()
    
    
    def clean(self):
        """ clean method is called automatically for each save in admin"""
        
        #when saving for the first time only, put this page last in order 
        if not self.id:
            # get max value of order for current pages.
            try:            
                max_order = Page.objects.filter(comicsite__pk=self.comicsite.pk).aggregate(Max('order'))                
            except ObjectDoesNotExist :
                max_order = None
                                        
            if max_order["order__max"] == None:
                self.order = 1
            else:
                self.order = max_order["order__max"] + 1
      
    
    
    def rawHTML(self):
        """Display html of this page as html. This uses the mark_safe django method to allow direct html rendering"""
        #TODO : do checking for scripts and hacks here? 
        return mark_safe(self.html)
    
    def rawHTMLrendered(self):
        """Display raw html, but render any template tags found using django's template system """
    
    def move(self, move):
        if move == 'UP':
            mm = Page.objects.get(comicsite=self.comicsite,order=self.order-1)
            mm.order += 1
            mm.save()
            self.order -= 1
            self.save()
        if move == 'DOWN':
            mm = Page.objects.get(comicsite=self.comicsite,order=self.order+1)
            mm.order -= 1
            mm.save()
            self.order += 1
            self.save()
        if move == 'FIRST':
            raise NotImplementedError("Somebody should implement this!")
        if move == 'LAST':
            raise NotImplementedError("Somebody should implement this!")

    
    class Meta(ComicSiteModel.Meta):
        """special class holding meta info for this class"""
        # make sure a single site never has two pages with the same name because page names
        # are used as keys in urls
        unique_together = (("comicsite", "title"),)
         
        # when getting a list of these objects this ordering is used
        ordering = ['comicsite','order']        


class ErrorPage(Page):
    """ Just the same as a Page, just that it does not display an edit button as admin"""
    is_error_page=True
    
    def can_be_viewed_by(self,user):
        """ overwrites Page class method. Errorpages can always be viewed"""
        return True
    
    class Meta:
       abstract = True  #error pages should only be generated on the fly currently. 
       
    

class UploadModel(ComicSiteModel):
        
    file = models.FileField(upload_to=giveFileUploadDestinationPath)
    
    
    @property    
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]
    
    class Meta(ComicSiteModel.Meta):
        verbose_name = "uploaded file"
        verbose_name_plural = "uploaded files"
        

    
class Dataset(ComicSiteModel):
    """
    Collection of files
    """    
    description = models.TextField()
    
    
       
    @property
    def cleantitle(self):
        return re.sub('[\[\]/{}., ]+', '',self.title)       
                
    class Meta:
       abstract = True
         
    
class FileSystemDataset(Dataset):
    """
    A folder location on disk
    """
    folder = models.FilePathField()
    folder_prefix = "datasets/"  # default initial subfolder to save datasets in, can be overwritten later on     
        
    def get_all_files(self):
        """ return array of all files in this folder
        """        
        dp = FileSystemDataProvider.FileSystemDataProvider(self.folder)
        filenames = dp.getFileNames()
        htmlOut = "available files:"+", ".join(filenames)
        return htmlOut

    
    def save_default(self,firstcreation):
        pdb.set_trace()
        
        if firstcreation:
            # initialize data dir 
            data_dir = self.get_default_data_dir()
            self.folder = data_dir            
        else:
            # take possibly edited value from form, keep self.folder.
            pass                                          
        self.ensure_dir(self.get_full_folder_path())        
        
            
        
    def get_full_folder_path(self):
        """ Return full path of the folder in which this datasets files reside """
        data_dir_path = os.path.join(settings.MEDIA_ROOT,self.folder)
        return data_dir_path
    
    def get_default_data_dir(self):
        """ In which dir should this dataset be located by default? Return path relative to MEDIA_ROOT  
        """                        
        data_dir_path = os.path.join(self.comicsite.short_name,self.folder_prefix,self.cleantitle)
        return data_dir_path
        
    def get_template_tag(self):
        """ Return the django template tag that can be used in page text to render this dataset on the page"""
        return "{% dataset " + self.cleantitle + " %}"
        
    def ensure_dir(self,dir):
        if not os.path.exists(dir):
            os.makedirs(dir)        


        
     