from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=3,
            max=100
        )
    )

    category = fields.Str(required=True)

    equipment_needed = fields.Bool(required=True)

    @validates("category")
    def validate_category(self, value, **kwargs):

        allowed = {
            "Strength",
            "Cardio",
            "Flexibility",
            "Balance"
        }

        if value.title() not in allowed:
            raise ValidationError(
                f"Category must be one of {allowed}"
            )

class WorkoutSchema(Schema):

    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(required=True)

    notes = fields.Str()

    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):

        if value <= 0:
            raise ValidationError(
                "Duration must be greater than zero."
            )

class WorkoutExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)

    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(allow_none=True)

    sets = fields.Int(allow_none=True)

    duration_seconds = fields.Int(allow_none=True)

    @validates("reps")
    def validate_reps(self, value, **kwargs):

        if value is not None and value <= 0:
            raise ValidationError(
                "Reps must be greater than zero."
            )

    @validates("sets")
    def validate_sets(self, value, **kwargs):

        if value is not None and value <= 0:
            raise ValidationError(
                "Sets must be greater than zero."
            )

    @validates("duration_seconds")
    def validate_duration(self, value, **kwargs):

        if value is not None and value <= 0:
            raise ValidationError(
                "Duration seconds must be greater than zero."
            )

    

exercise_schema = ExerciseSchema()

exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()

workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

workout_exercises_schema = WorkoutExerciseSchema(many=True)