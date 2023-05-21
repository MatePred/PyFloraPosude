from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ModifyPLantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Plant name"})
    photoURL = StringField('photoURL', validators=[DataRequired()], render_kw={"placeholder": "Photo URL"})
    humidityValue = StringField('humidityValue', validators=[DataRequired()], render_kw={"placeholder": "Humidity value"})
    tempValue = StringField('tempValue', validators=[DataRequired()], render_kw={"placeholder": "Temperature value"})
    lightValue = StringField('lightValue', validators=[DataRequired()], render_kw={"placeholder": "Light value"})