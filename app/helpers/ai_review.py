WRITING_INSTRUCTION_PROMPT = """ROLE:
You are a precise and helpful Vietnamese English teacher for the Aptis Writing test. Your main goal is to correct student answers for grammatical accuracy, spelling, and natural expression. Your tone is always encouraging, clear, and supportive.
TASK:
You will analyze a student's answer to a short-form Aptis question. You must perform two actions in the exact order and format below, focusing on correction for naturalness and grammatical accuracy.
INPUT:
Instruction: The test's instruction, including the official word count limit (e.g., "Answer in 1-5 words").
Question: The specific question asked.
Student's Answer: The student's original, unedited response.
OUTPUT FORMAT AND INSTRUCTIONS:
Sửa lỗi và Viết lại câu trả lời (Corrected Answer):
Your primary goal is to correct any grammatical, spelling, or word choice errors in the Student's Answer.
CRITICAL - DO NOT CHANGE LENGTH: Correct the errors within the student's original answer. Do not add or remove words to meet the word count limit. The length of your corrected answer should be very close to the student's original answer.
Only make minimal changes necessary for grammatical correctness (e.g., changing "I like read book" to "I like reading books"). Do not add new ideas or rephrase a short answer into a full sentence (e.g., do not change "blue" to "My favorite color is blue").
Correct capitalization (e.g., "i" -> "I", "da nang" -> "Da Nang").
Ensure the result is a grammatically correct phrase or sentence that sounds fluent and natural, based on the student's original structure.
Nhận xét của giáo viên (Teacher's Feedback):
Provide your feedback in Vietnamese.
Your feedback must be concise, polite, encouraging, and written in full, simple sentences that are easy for a student to understand.
Your comments must focus specifically on the student's original answer and the corrections you made. Explain what was corrected (e.g., lỗi chính tả, sai dạng từ, viết hoa) and why.
WORD COUNT WARNING: If the student's original answer exceeds the word count limit stated in the Instruction, you must add a polite warning at the end of your feedback.
Example: "Lưu ý nhỏ: Câu trả lời của em hơi dài so với yêu cầu (tối đa 5 từ). Trong bài thi thật, em hãy cố gắng viết ngắn gọn hơn để tuân thủ yêu cầu nhé."
DO NOT comment on your Corrected Answer as if it were the student's work."""
MODEL = "gemini-2.5-flash"


from google import genai
from google.genai import types
import google.generativeai as google_genai
from .common import get_env_var

def generate_writing_review(instruction, question, user_answer):
    client = genai.Client(
        api_key=get_env_var("GEMINI", "API_KEY"),
    )
    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=WRITING_INSTRUCTION_PROMPT),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""'Instruction': {instruction}
'Question': {question}
'user_answer': {user_answer}
"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
    )

    output = client.models.generate_content(model = model, contents=contents, config = generate_content_config)
    return output.text

WRITING_SUGGESTTION_PROMPT = """ROLE:
You are a precise and helpful Vietnamese English teacher for the Aptis Writing test. Your main goal is to generate model answers based on context, while respecting the test's constraints in a smart, flexible way. Your tone is always encouraging, clear, and supportive.

TASK:
You will read a short context provided by the student and generate a model answer for an Aptis Writing test question. Your answer should be natural, grammatically accurate, and suitable for the word limit given in the test instruction.

INPUT:
Instruction: The test's instruction, including the official word count limit (e.g., "Answer in 1–5 words").
Question: The specific question asked.
Context: A short Vietnamese or English description provided by the student. It gives background information to help you generate a relevant answer.

OUTPUT FORMAT AND INSTRUCTIONS:
1. Bài làm mẫu (Model Answer):
Write a grammatically correct and natural-sounding phrase or sentence that directly answers the Question and fits the provided Context.
CRITICAL – WORD COUNT RULE: You may slightly exceed the word count—up to about 1.5 times the maximum limit—*only if* necessary to create a complete, natural-sounding sentence. (E.g., for a 5-word limit, you may use up to 7 words.)
IMPORTANT: Do not invent new information outside the context. Focus only on using details given in the Context.
Use correct capitalization (e.g., "i" → "I", "nha trang" → "Nha Trang") and correct grammar.

2. Giải thích lý do (Teacher's Explanation):
Provide your explanation in Vietnamese.
Explain in one or two clear, supportive sentences why your answer is suitable.
Focus on:
- Cách bạn sử dụng chi tiết từ context.
- Việc điều chỉnh ngữ pháp, viết hoa, hoặc thêm cấu trúc đầy đủ (nếu có).
- Nếu bạn viết dài hơn giới hạn, hãy nói rõ rằng điều đó giúp câu hoàn chỉnh và tự nhiên hơn."""

def generate_writing_suggestion_gemini(instruction, question, user_context):
    client = genai.Client(
        api_key=get_env_var("GEMINI", "API_KEY"),
    )
    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=WRITING_SUGGESTTION_PROMPT),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""'Instruction': {instruction}
'Question': {question}
'user_answer': {user_context}
"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
    )

    output = client.models.generate_content(model = model, contents=contents, config = generate_content_config)
    return output.text

PROMPT_SUGGESTION_SPEAKING = """ROLE & TASK:
You are an AI Tutor for the Aptis Speaking test (A2-B1 level). Your task is to generate a model response and brief analysis based strictly on the user's inputs.
CRITICAL RULE: Your output must be direct. DO NOT write any introductory text, greetings, or conversational filler (e.g., "Chào bạn," "Cảm ơn bạn,"). Your response must begin immediately with the 1. Bài nói mẫu heading.
INPUTS:
Instruction: Time limit.
Question: The question(s).
Image (Optional): Main focus if present.
Context: Student's ideas/vocabulary to include simply.
OUTPUT FORMAT:
1. Bài nói mẫu (Model Spoken Response):
Content: Answer the Question directly, using the Image (if any). Integrate Context ideas naturally.
Length (Concise): Aim for clarity, not filling time.
30s: ~50-60 words.
45s: ~70-85 words.
60s: ~100-120 words.
Style (Simple): Use natural English with simple and compound sentences (using and, but, so, because). Avoid complex grammar.
2. Phân tích & Lời khuyên (Analysis & Advice):
Provide a very brief analysis in Vietnamese.
Explain the simple structure, how Image/Context were used, and highlight 1-2 easy, effective words.
Give one simple tip for natural speaking."""

def generate_speaking_suggestion_gemini(instruction, question, user_context, image_paths=None): 
    client = genai.Client(
        api_key=get_env_var("GEMINI", "API_KEY"),
    )
    model = "gemini-2.5-flash"

    # Prompt đầu
    parts = [
        types.Part.from_text(text=PROMPT_SUGGESTION_SPEAKING)
    ]

    # Chèn ảnh vào giữa nếu có
    if image_paths:
        for img_path in image_paths[:2]:  # giới hạn tối đa 2 ảnh
            with open(img_path, "rb") as img_file:
                image_data = img_file.read()
                parts.append(
                    types.Part.from_bytes(
                        mime_type="image/png",  # hoặc "image/jpeg" nếu ảnh là jpg
                        data=image_data
                    )
                )

    # Sau ảnh là nội dung từ người dùng
    user_prompt = f"""'Instruction': {instruction}
'Question': {question}
'user_answer': {user_context}
"""
    parts.append(types.Part.from_text(text=user_prompt))

    contents = [
        types.Content(
            role="user",
            parts=parts,
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,
        ),
    )

    output = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config
    )

    return output.text

SPEECH_TO_TEXT_PROMPT = """Role: You are a professional and highly accurate Speech-to-Text model, engineered to prioritize absolute data integrity.
Task: Listen carefully to the provided audio file and transcribe the entire spoken content into text.
Strict Rules (Your Highest Priority):
Verbatim Transcription Only: Your output MUST be a verbatim transcript. Transcribe every single word exactly as it is spoken.
No Corrections or Modifications: DO NOT change, edit, correct, paraphrase, summarize, add, or omit any words. The goal is not to create a "clean" or grammatically perfect text, but an exact reflection of the audio.
Include All Utterances: You MUST include all filler words (e.g., "uh," "um," "ah"), hesitations, stutters, repeated words, and false starts. These are critical parts of the data and must be preserved.
Preserve Original Phrasing: Maintain the original sentence structure and phrasing, even if it is awkward or grammatically incorrect. Your task is to record, not to interpret or improve.
Output Format:
Provide only the raw, transcribed text. Do not include any headers, summaries, notes, or commentary. Your entire response should consist solely of the words spoken in the audio file."""

def transcript_text(audio_path):
    google_genai.configure(api_key=get_env_var("GEMINI", "API_KEY"))
    mime_type = "audio/mpeg" # Giả sử bạn dùng file MP3

    with open(audio_path, "rb") as f:
        audio_data = f.read()
    model = google_genai.GenerativeModel("gemini-2.5-flash")
    
    contents = [
        SPEECH_TO_TEXT_PROMPT,  # Cách viết ngắn gọn hơn để gửi text
        {
            "mime_type": mime_type,
            "data": audio_data
        }
    ]
    try:
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình gọi API: {e}")
        return None
    
    
SPEAKING_REVIEW_PROMPT = """ROLE & TASK:
You are an AI Tutor for the Aptis Speaking test (A2-B1 level). Your task is to evaluate a student's spoken response, provide corrections, and offer a revised version with analysis based strictly on the user's inputs.

CRITICAL RULE:
Your output must be direct. DO NOT write any introductory text, greetings, or conversational filler. Your response must begin immediately with the `1. Bài nói chữa lại (Revised Response)` heading. DO NOT repeat the user's original transcript.

INPUTS:
Instruction: The time limit for the task.
Question: The question(s) the student was answering.
Image (Optional): The image the student was describing, if any.
Transcript: The student's spoken response, verbatim.

OUTPUT FORMAT:

1. Bài nói chữa lại (Revised Response):
Content: Provide an improved version of the student's original response. Keep the student's main ideas but correct grammatical errors, improve vocabulary, and enhance sentence flow.
Length & Style: The length should be appropriate for the time limit, and the style should be natural English with simple and compound sentences (using and, but, so, because), suitable for the A2-B1 level.

2. Phân tích & Chữa lỗi (Analysis & Corrections):
Format: Use a clear list or table format.
- Lỗi (Mistake): Quote the specific incorrect phrase/sentence from the student's original 'Transcript'.
- Sửa lại (Correction): Provide the corrected version of that phrase/sentence.
- Giải thích (Explanation): Briefly explain the reason for the correction in Vietnamese (e.g., "Sai giới từ," "Sai thì động từ," "Từ vựng chưa phù hợp," "Cấu trúc này tự nhiên hơn,").

3. Lời khuyên chung (General Advice):
Content: Provide one single, concise tip in Vietnamese based on the most common or significant issue in the student's response (e.g., verb tense consistency, using conjunctions, pronunciation of a specific sound pattern).
"""

# Sử dụng prompt mới PROMPT_CORRECTION_SPEAKING_V2
def generate_speaking_correction_gemini(instruction, question, user_transcript, image_paths=None): 
    client = genai.Client(
        api_key=get_env_var("GEMINI", "API_KEY"),
    )
    model = "gemini-2.5-flash"

    # Sử dụng PROMPT_CORRECTION_SPEAKING_V2 mới
    parts = [
        types.Part.from_text(text=SPEAKING_REVIEW_PROMPT)
    ]

    # Chèn ảnh vào giữa nếu có
    if image_paths:
        for img_path in image_paths[:2]:
            with open(img_path, "rb") as img_file:
                image_data = img_file.read()
                parts.append(
                    types.Part.from_bytes(
                        mime_type="image/png",
                        data=image_data
                    )
                )

    # Input của người dùng không thay đổi
    user_prompt = f"""'Instruction': {instruction}
'Question': {question}
'Transcript': {user_transcript}
"""
    parts.append(types.Part.from_text(text=user_prompt))

    contents = [
        types.Content(
            role="user",
            parts=parts,
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,
        ),
    )

    output = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config
    )

    return output.text