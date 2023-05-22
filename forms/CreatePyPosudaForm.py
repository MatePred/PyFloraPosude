from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class CreatePyPosudaForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Plant name"})
    plant_name = SelectField('Plant', choices=[], validators=[DataRequired()], render_kw={"placeholder": "Select plant"})