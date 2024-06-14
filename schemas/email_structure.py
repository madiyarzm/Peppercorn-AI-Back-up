from wsgiref import validate
import jsonschema
from pydantic import BaseModel, Field
from typing import List, Optional

class TextProperties(BaseModel):
    text: str
    font_family: Optional[str] = "Arial, sans-serif"
    font_size: Optional[str] = "14px"
    text_color: Optional[str] = "#000000"
    text_align: Optional[str] = "left"
    line_height: Optional[str] = "normal"
    letter_spacing: Optional[str] = "normal"
    text_decoration: Optional[str] = None
    font_weight: Optional[str] = "normal"
    font_style: Optional[str] = "normal"
    text_transform: Optional[str] = "none"

class LayoutProperties(BaseModel):
    width: Optional[str] = "auto"
    height: Optional[str] = "auto"
    margin: Optional[str] = "0"
    padding: Optional[str] = "0"
    border: Optional[str] = "none"
    display: Optional[str] = "block"
    flex_direction: Optional[str] = None
    justify_content: Optional[str] = None
    align_items: Optional[str] = None
    background_color: Optional[str] = "#FFFFFF"
    box_shadow: Optional[str] = None

class Structure(BaseModel):
    layout_properties: LayoutProperties
    text_properties: List[TextProperties]
    elements: List["Structure"] = []

class Section(BaseModel):
    title: Optional[str]
    structures: List[Structure]

class EmailScaffold(BaseModel):
    sections: List[Section]
    overall_layout: LayoutProperties
    explanation: Optional[str]
    followup_question_to_client: Optional[str] = Field(
        "Follow-up Question to Client given what you want to do next"
    )

    class Config:
        schema_extra = {
            "example": {
                "sections": [
                    {
                        "title": "Header",
                        "structures": [
                            {
                                "layout_properties": {
                                    "background_color": "#f3f3f3",
                                    "padding": "20px",
                                    "text_align": "center"
                                },
                                "text_properties": [
                                    {
                                        "text": "Welcome to Our Newsletter!",
                                        "font_size": "24px",
                                        "text_color": "#333333",
                                        "font_weight": "bold"
                                    }
                                ],
                                "elements": []
                            }
                        ]
                    }
                ],
                "overall_layout": {
                    "background_color": "#eeeeee",
                    "margin": "0 auto",
                    "width": "600px",
                    "padding": "0"
                },
                "explanation": "This is an example email scaffold.",
                "followup_question_to_client": "What would you like to do next?"
            }
        }

