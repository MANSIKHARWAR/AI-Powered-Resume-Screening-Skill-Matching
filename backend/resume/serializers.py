from rest_framework import serializers

class ResumeSerializer(serializers.Serializer):
    resume_text = serializers.CharField()
    job_description = serializers.CharField()
