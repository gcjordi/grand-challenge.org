from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django_extensions.db.models import TitleSlugDescriptionModel
from guardian.shortcuts import assign_perm

from grandchallenge.core.models import UUIDModel
from grandchallenge.core.validators import JSONSchemaValidator
from grandchallenge.subdomains.utils import reverse

OVERLAY_SEGMENTS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The Overlay Segments Schema",
    "description": "Define the overlay segments for the LUT.",
    "items": {
        "$id": "#/items",
        "type": "object",
        "title": "The Segment Schema",
        "description": "Defines what each segment of the LUT represents.",
        "default": {},
        "examples": [
            {
                "name": "Metastasis",
                "voxel_value": 1,
                "visible": True,
                "metric_template": "{{metrics.volumes[0]}} mm³",
            }
        ],
        "required": ["voxel_value", "name", "visible"],
        "additionalProperties": False,
        "properties": {
            "voxel_value": {
                "$id": "#/items/properties/voxel_value",
                "type": "integer",
                "title": "The Voxel Value Schema",
                "description": "The value of the LUT for this segment.",
                "default": 0,
                "examples": [1],
            },
            "name": {
                "$id": "#/items/properties/name",
                "type": "string",
                "title": "The Name Schema",
                "description": "What this segment should be called.",
                "default": "",
                "examples": ["Metastasis"],
            },
            "visible": {
                "$id": "#/items/properties/visible",
                "type": "boolean",
                "title": "The Visible Schema",
                "description": "Whether this segment is visible by default.",
                "default": True,
                "examples": [True],
            },
            "metric_template": {
                "$id": "#/items/properties/metric_template",
                "type": "string",
                "title": "The Metric Template Schema",
                "description": "The jinja template to determine which property from the results.json should be used as the label text.",
                "default": "",
                "examples": ["{{metrics.volumes[0]}} mm³"],
            },
        },
    },
}

KEY_BINDINGS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema",
    "$id": "http://example.com/example.json",
    "type": "array",
    "title": "The Key Bindings Schema",
    "description": "Define the key bindings for the workstation.",
    "items": {
        "$id": "#/items",
        "type": "object",
        "title": "The Key Binding Schema",
        "description": "Defines a key binding for a command.",
        "default": {},
        "examples": [
            {
                "key": "ctrl+shift+k",
                "command": "editor.action.deleteLines",
                "when": "editorTextFocus",
            }
        ],
        "required": ["key", "command"],
        "additionalProperties": False,
        "properties": {
            "key": {
                "$id": "#/items/properties/key",
                "type": "string",
                "title": "The Key Schema",
                "description": "The keys used for this binding.",
                "default": "",
                "examples": ["ctrl+shift+k"],
            },
            "command": {
                "$id": "#/items/properties/command",
                "type": "string",
                "title": "The Command Schema",
                "description": "The command called by this binding.",
                "default": "",
                "examples": ["editor.action.deleteLines"],
            },
            "when": {
                "$id": "#/items/properties/when",
                "type": "string",
                "title": "The When Schema",
                "description": "The condition that must be met for this command to be called.",
                "default": "",
                "examples": ["editorTextFocus"],
            },
        },
    },
}


class WorkstationConfig(TitleSlugDescriptionModel, UUIDModel):
    ORIENTATION_AXIAL = "A"
    ORIENTATION_CORONAL = "C"
    ORIENTATION_SAGITTAL = "S"

    ORIENTATION_CHOICES = (
        (ORIENTATION_AXIAL, "Axial"),
        (ORIENTATION_CORONAL, "Coronal"),
        (ORIENTATION_SAGITTAL, "Sagittal"),
    )

    SLAB_RENDER_METHOD_MAXIMUM = "MAX"
    SLAB_RENDER_METHOD_MINIMUM = "MIN"
    SLAB_RENDER_METHOD_AVERAGE = "AVG"

    SLAB_RENDER_METHOD_CHOICES = (
        (SLAB_RENDER_METHOD_MAXIMUM, "Maximum"),
        (SLAB_RENDER_METHOD_MINIMUM, "Minimum"),
        (SLAB_RENDER_METHOD_AVERAGE, "Average"),
    )

    IMAGE_INTERPOLATION_TYPE_NEAREST = "NN"
    IMAGE_INTERPOLATION_TYPE_TRILINEAR = "TL"
    IMAGE_INTERPOLATION_TYPE_CHOICES = (
        (IMAGE_INTERPOLATION_TYPE_NEAREST, "NearestNeighbor"),
        (IMAGE_INTERPOLATION_TYPE_TRILINEAR, "Trilinear"),
    )

    creator = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL
    )

    window_presets = models.ManyToManyField(
        to="WindowPreset",
        blank=True,
        related_name="workstation_window_presets",
    )
    default_window_preset = models.ForeignKey(
        to="WindowPreset",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="workstation_default_window_presets",
    )

    # 4 digits, 2 decimal places, 0.01 min, 99.99 max
    default_slab_thickness_mm = models.DecimalField(
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=0.01)],
    )
    default_slab_render_method = models.CharField(
        max_length=3, choices=SLAB_RENDER_METHOD_CHOICES, blank=True
    )

    default_orientation = models.CharField(
        max_length=1, choices=ORIENTATION_CHOICES, blank=True
    )

    default_overlay_lut = models.ForeignKey(
        to="LookUpTable", blank=True, null=True, on_delete=models.SET_NULL
    )
    default_overlay_interpolation = models.CharField(
        max_length=2,
        choices=IMAGE_INTERPOLATION_TYPE_CHOICES,
        default=IMAGE_INTERPOLATION_TYPE_NEAREST,
        blank=True,
    )
    # 3 digits, 2 decimal places, 0.00 min, 1.00 max
    default_overlay_alpha = models.DecimalField(
        blank=True,
        null=True,
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(limit_value=0.00),
            MaxValueValidator(limit_value=1.00),
        ],
    )

    overlay_segments = models.JSONField(
        default=list,
        blank=True,
        validators=[JSONSchemaValidator(schema=OVERLAY_SEGMENTS_SCHEMA)],
    )

    key_bindings = models.JSONField(
        default=list,
        blank=True,
        validators=[JSONSchemaValidator(schema=KEY_BINDINGS_SCHEMA)],
    )

    # 4 digits, 2 decimal places, 0.01 min, 99.99 max
    default_zoom_scale = models.DecimalField(
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=0.01)],
    )

    show_image_info_plugin = models.BooleanField(default=True)
    show_display_plugin = models.BooleanField(default=True)
    show_invert_tool = models.BooleanField(default=True)
    show_flip_tool = models.BooleanField(default=True)
    show_window_level_tool = models.BooleanField(default=True)
    show_reset_tool = models.BooleanField(default=True)

    class Meta(TitleSlugDescriptionModel.Meta, UUIDModel.Meta):
        ordering = ("created", "creator")

    def __str__(self):
        return f"{self.title} (created by {self.creator})"

    def get_absolute_url(self):
        return reverse(
            "workstation-configs:detail", kwargs={"slug": self.slug}
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.creator:
            assign_perm(
                f"{self._meta.app_label}.change_{self._meta.model_name}",
                self.creator,
                self,
            )


class WindowPreset(TitleSlugDescriptionModel):
    width = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=1)]
    )
    center = models.IntegerField()

    class Meta(TitleSlugDescriptionModel.Meta):
        ordering = ("title",)

    def __str__(self):
        return f"{self.title} (center {self.center}, width {self.width})"


class LookUpTable(TitleSlugDescriptionModel):
    COLOR_INTERPOLATION_RGB = "RGB"
    COLOR_INTERPOLATION_HLS = "HLS"
    COLOR_INTERPOLATION_HLS_POS = "HLSpos"
    COLOR_INTERPOLATION_HLS_NEG = "HLSneg"
    COLOR_INTERPOLATION_CONSTANT = "Constant"
    COLOR_INTERPOLATION_CHOICES = (
        (COLOR_INTERPOLATION_RGB, "RGB"),
        (COLOR_INTERPOLATION_HLS, "HLS"),
        (COLOR_INTERPOLATION_HLS_POS, "HLS Positive"),
        (COLOR_INTERPOLATION_HLS_NEG, "HLS Negative"),
        (COLOR_INTERPOLATION_CONSTANT, "Constant"),
    )

    # These regex reflect what MeVisLab accepts as color and alpha strings
    # and kept for compatibility. Probably, we want to clean these fields up
    # later for use elsewhere.
    COLOR_REGEX = r"^\[(?:((?: ?-?\d*(?:\.\d+)? ){3}(?:-?\d*(?:\.\d+)?)) ?, ?)+((?:-?\d*(?:\.\d+)? ){3}(?:\d*(:?\.\d+)? ?))\]$"
    ALPHA_REGEX = r"^\[(?:((?: ?-?\d*(?:\.\d+)? ){1}(?:-?\d*(?:\.\d+)?)) ?, ?)+((?:-?\d*(?:\.\d+)? ){1}(?:\d*(:?\.\d+)? ?))\]$"

    color = models.TextField(validators=[RegexValidator(regex=COLOR_REGEX)])
    alpha = models.TextField(validators=[RegexValidator(regex=ALPHA_REGEX)])
    color_invert = models.TextField(
        blank=True, validators=[RegexValidator(regex=COLOR_REGEX)]
    )
    alpha_invert = models.TextField(
        blank=True, validators=[RegexValidator(regex=ALPHA_REGEX)]
    )

    range_min = models.SmallIntegerField(default=0)
    range_max = models.SmallIntegerField(default=4095)
    relative = models.BooleanField(default=False)

    color_interpolation = models.CharField(
        max_length=8,
        choices=COLOR_INTERPOLATION_CHOICES,
        default=COLOR_INTERPOLATION_RGB,
    )
    color_interpolation_invert = models.CharField(
        max_length=8,
        choices=COLOR_INTERPOLATION_CHOICES,
        default=COLOR_INTERPOLATION_RGB,
    )

    class Meta(TitleSlugDescriptionModel.Meta):
        ordering = ("title",)

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        color_points = len(self.color.split(","))
        alpha_points = len(self.alpha.split(","))
        if color_points != alpha_points:
            raise ValidationError(
                "The color and alpha LUT should have the same number of elements"
            )

        if self.color_invert or self.alpha_invert:
            color_invert_points = len(self.color_invert.split(","))
            alpha_invert_points = len(self.alpha_invert.split(","))
            if color_invert_points != alpha_invert_points:
                raise ValidationError(
                    "The color invert and alpha invert LUT should have the same number of elements"
                )
