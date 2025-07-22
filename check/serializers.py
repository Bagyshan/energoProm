from rest_framework import serializers
from .models import Check

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'
        read_only_fields = (
            'previous_check',
            'previous_check_date',
            'period_day_count',
            'total_sum',
            'consumption',
            'amount_for_expenses',
            'created_at',
            'updated_at',
        )

