# Generated by Django 3.0.5 on 2020-04-21 13:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations

import grandchallenge.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ("reader_studies", "0016_auto_20200406_1334"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="answer",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                null=True,
                validators=[
                    grandchallenge.core.validators.JSONSchemaValidator(
                        schema={
                            "$schema": "http://json-schema.org/draft-07/schema#",
                            "anyOf": [
                                {"$ref": "#/definitions/null"},
                                {"$ref": "#/definitions/STXT"},
                                {"$ref": "#/definitions/MTXT"},
                                {"$ref": "#/definitions/BOOL"},
                                {"$ref": "#/definitions/HEAD"},
                                {"$ref": "#/definitions/2DBB"},
                                {"$ref": "#/definitions/DIST"},
                                {"$ref": "#/definitions/MDIS"},
                                {"$ref": "#/definitions/POIN"},
                                {"$ref": "#/definitions/MPOI"},
                                {"$ref": "#/definitions/POLY"},
                                {"$ref": "#/definitions/MPOL"},
                                {"$ref": "#/definitions/CHOI"},
                                {"$ref": "#/definitions/MCHO"},
                                {"$ref": "#/definitions/MCHD"},
                            ],
                            "definitions": {
                                "2DBB": {
                                    "properties": {
                                        "corners": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "maxItems": 4,
                                            "minItems": 4,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {"enum": ["2D bounding box"]},
                                    },
                                    "required": ["version", "type", "corners"],
                                    "type": "object",
                                },
                                "BOOL": {"type": "boolean"},
                                "CHOI": {"type": "number"},
                                "DIST": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Distance measurement"]
                                        },
                                    },
                                    "required": [
                                        "version",
                                        "type",
                                        "start",
                                        "end",
                                    ],
                                    "type": "object",
                                },
                                "HEAD": {"type": "null"},
                                "MCHD": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MCHO": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MDIS": {
                                    "properties": {
                                        "lines": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/line-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {
                                            "enum": [
                                                "Multiple distance measurements"
                                            ]
                                        },
                                    },
                                    "required": ["version", "type", "lines"],
                                    "type": "object",
                                },
                                "MPOI": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "points": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/point-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Multiple points"]},
                                    },
                                    "required": ["version", "type", "points"],
                                    "type": "object",
                                },
                                "MPOL": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "polygons": {
                                            "items": {
                                                "$ref": "#/definitions/polygon-object"
                                            },
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Multiple polygons"]
                                        },
                                    },
                                    "required": [
                                        "type",
                                        "version",
                                        "polygons",
                                    ],
                                    "type": "object",
                                },
                                "MTXT": {"type": "string"},
                                "POIN": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Point"]},
                                    },
                                    "required": ["version", "type", "point"],
                                    "type": "object",
                                },
                                "POLY": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                        "version",
                                    ],
                                    "type": "object",
                                },
                                "STXT": {"type": "string"},
                                "line-object": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["start", "end"],
                                    "type": "object",
                                },
                                "null": {"type": "null"},
                                "point-object": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["point"],
                                    "type": "object",
                                },
                                "polygon-object": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                    ],
                                    "type": "object",
                                },
                            },
                            "properties": {
                                "version": {
                                    "additionalProperties": {"type": "number"},
                                    "required": ["major", "minor"],
                                    "type": "object",
                                }
                            },
                        }
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="historicalanswer",
            name="answer",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                null=True,
                validators=[
                    grandchallenge.core.validators.JSONSchemaValidator(
                        schema={
                            "$schema": "http://json-schema.org/draft-07/schema#",
                            "anyOf": [
                                {"$ref": "#/definitions/null"},
                                {"$ref": "#/definitions/STXT"},
                                {"$ref": "#/definitions/MTXT"},
                                {"$ref": "#/definitions/BOOL"},
                                {"$ref": "#/definitions/HEAD"},
                                {"$ref": "#/definitions/2DBB"},
                                {"$ref": "#/definitions/DIST"},
                                {"$ref": "#/definitions/MDIS"},
                                {"$ref": "#/definitions/POIN"},
                                {"$ref": "#/definitions/MPOI"},
                                {"$ref": "#/definitions/POLY"},
                                {"$ref": "#/definitions/MPOL"},
                                {"$ref": "#/definitions/CHOI"},
                                {"$ref": "#/definitions/MCHO"},
                                {"$ref": "#/definitions/MCHD"},
                            ],
                            "definitions": {
                                "2DBB": {
                                    "properties": {
                                        "corners": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "maxItems": 4,
                                            "minItems": 4,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {"enum": ["2D bounding box"]},
                                    },
                                    "required": ["version", "type", "corners"],
                                    "type": "object",
                                },
                                "BOOL": {"type": "boolean"},
                                "CHOI": {"type": "number"},
                                "DIST": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Distance measurement"]
                                        },
                                    },
                                    "required": [
                                        "version",
                                        "type",
                                        "start",
                                        "end",
                                    ],
                                    "type": "object",
                                },
                                "HEAD": {"type": "null"},
                                "MCHD": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MCHO": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MDIS": {
                                    "properties": {
                                        "lines": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/line-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {
                                            "enum": [
                                                "Multiple distance measurements"
                                            ]
                                        },
                                    },
                                    "required": ["version", "type", "lines"],
                                    "type": "object",
                                },
                                "MPOI": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "points": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/point-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Multiple points"]},
                                    },
                                    "required": ["version", "type", "points"],
                                    "type": "object",
                                },
                                "MPOL": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "polygons": {
                                            "items": {
                                                "$ref": "#/definitions/polygon-object"
                                            },
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Multiple polygons"]
                                        },
                                    },
                                    "required": [
                                        "type",
                                        "version",
                                        "polygons",
                                    ],
                                    "type": "object",
                                },
                                "MTXT": {"type": "string"},
                                "POIN": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Point"]},
                                    },
                                    "required": ["version", "type", "point"],
                                    "type": "object",
                                },
                                "POLY": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                        "version",
                                    ],
                                    "type": "object",
                                },
                                "STXT": {"type": "string"},
                                "line-object": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["start", "end"],
                                    "type": "object",
                                },
                                "null": {"type": "null"},
                                "point-object": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["point"],
                                    "type": "object",
                                },
                                "polygon-object": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                    ],
                                    "type": "object",
                                },
                            },
                            "properties": {
                                "version": {
                                    "additionalProperties": {"type": "number"},
                                    "required": ["major", "minor"],
                                    "type": "object",
                                }
                            },
                        }
                    )
                ],
            ),
        ),
    ]