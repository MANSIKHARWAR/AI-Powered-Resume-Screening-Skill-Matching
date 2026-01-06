from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from resume.serializers import ResumeSerializer
from .bert_model import calculate_similarity
import PyPDF2

# -------------------------
# TEST API (Health Check)
# -------------------------
@api_view(['GET'])
def test_api(request):
    """
    Simple health check endpoint.
    """
    return Response({"status": "Backend is running ✅"})


# -------------------------
# COMPARE RESUME TEXT
# -------------------------
@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def compare_resume(request):
    # Debug: see what backend is actually receiving
    print("REQUEST DATA:", request.data)

    serializer = ResumeSerializer(data=request.data)

    if serializer.is_valid():
        resume_text = serializer.validated_data['resume_text']
        job_desc = serializer.validated_data['job_description']

        score = calculate_similarity(resume_text, job_desc)

        return Response({"match_percentage": score})

    return Response({
        "error": "Invalid request format",
        "expected_format": {
            "resume_text": "string",
            "job_description": "string"
        },
        "received_data": request.data,
        "details": serializer.errors
    }, status=400)

# -------------------------
# UPLOAD PDF RESUME
# -------------------------
@api_view(['POST'])
def upload_resume(request):
    """
    Accepts a PDF resume file, extracts text, and returns a preview.
    """
    if 'resume' not in request.FILES:
        return Response({"error": "No resume file uploaded"}, status=400)

    resume_file = request.FILES['resume']

    try:
        reader = PyPDF2.PdfReader(resume_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if not text.strip():
            return Response({"error": "Unable to extract text from PDF"}, status=400)

        return Response({
            "resume_text": text[:500]  # preview first 500 characters
        })

    except Exception as e:
        return Response({"error": f"Failed to read PDF: {str(e)}"}, status=500)
