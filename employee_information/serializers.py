from rest_framework import serializers
from .models import Staff

class StaffRegistrationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, required=True)  # 10-digit code for registration
    
    class Meta:
        model = Staff
        fields = ['surname', 'other_names', 'date_of_birth', 'id_photo', 'code']

    def validate_code(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Invalid code.")
        return value

    def create(self, validated_data):
        validated_data.pop('code')  # The code is validated but not saved
        employee_number = self.generate_employee_number()
        staff = Staff.objects.create(employee_number=employee_number, **validated_data)
        return staff
    
    def generate_employee_number(self):
        import random
        return str(random.randint(1000000000, 9999999999))
    

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['employee_number', 'surname', 'other_names', 'date_of_birth', 'id_photo']

class StaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['date_of_birth', 'id_photo']
