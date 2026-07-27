from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    name = fields.Str(required=True)

    category = fields.Str(required=True)

    equipment_needed = fields.Bool(required=True)

class WorkoutSchema(Schema):

    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(required=True)

    notes = fields.Str()

class WorkoutExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    workout_id = fields.Int(required=True)

    exercise_id = fields.Int(required=True)

    reps = fields.Int(allow_none=True)

    sets = fields.Int(allow_none=True)

    duration_seconds = fields.Int(allow_none=True)


exercise_schema = ExerciseSchema()

exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()

workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

workout_exercises_schema = WorkoutExerciseSchema(many=True)