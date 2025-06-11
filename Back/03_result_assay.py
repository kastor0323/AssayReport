from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

def evaluate_with_suggestions(job_title, position, qa_pairs):
    try:
        # ChatGPT에 전달할 프롬프트 구성
        prompt = f"""
        직무: {job_title}
        직위: {position}
        
        다음 자소서 답변을 평가하고 개선점을 제안해주세요:
        
        질문: {qa_pairs[0]['question']}
        답변: {qa_pairs[0]['answer']}
        
        다음 형식으로 평가해주세요:
        1. 답변의 장점
        2. 개선이 필요한 부분
        3. 구체적인 개선 제안
        """
        
        # ChatGPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 자소서 평가 전문가입니다. 구체적이고 실질적인 피드백을 제공해주세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        suggestions = response.choices[0].message.content
        
        return {
            "상세결과": [{
                "개선제안": suggestions
            }]
        }
        
    except Exception as e:
        print(f"Error in evaluate_with_suggestions: {str(e)}")
        return {"error": str(e)}

@app.route('/api/evaluate-with-suggestions', methods=['POST'])
def evaluate_suggestions():
    try:
        data = request.json
        job_title = data.get('직무')
        position = data.get('직위')
        qa_pairs = data.get('qa_pairs')
        
        if not all([job_title, position, qa_pairs]):
            return jsonify({"error": "필수 데이터가 누락되었습니다."}), 400
            
        result = evaluate_with_suggestions(job_title, position, qa_pairs)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 