"""faq Agent: 透過Rag檢索小三美日網店的基本資訊。"""
import os

from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

from dotenv import load_dotenv
from .prompts import return_instructions_faq, return_global_instructions_faq

load_dotenv()

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        '使用此工具從知識庫中檢索與小三美日相關的文檔和參考資料'
    ),
    rag_resources=[
        rag.RagResource(
            # please fill in your own rag corpus
            # here is a sample rag coprus for testing purpose
            # e.g. projects/123/locations/us-central1/ragCorpora/456
            rag_corpus=os.environ.get("RAG_CORPUS")
        )
    ],
    # 調整檢索參數以提高電商FAQ的相關性
    similarity_top_k=8,  # 保留8個相似文檔，適合電商多樣性問題
    vector_distance_threshold=0.68,  # 略微提高閾值，確保檢索結果更相關
)

root_agent = LlmAgent(
    # 考慮使用更高質量的模型
    model=os.getenv("FAQ_AGENT_MODEL"),
    name='faq_agent',
    instruction=return_instructions_faq(),
    global_instruction=return_global_instructions_faq(),
        tools=[
        ask_vertex_retrieval,
    ],
    # 添加生成設定，提高回答的穩定性和準確性
    generate_content_config=types.GenerateContentConfig(
        temperature=0.15,  # 進一步降低溫度，提高電商政策回答的一致性
        top_p=0.92,
        top_k=40,
        candidate_count=1,  # 只生成一個回答版本，確保政策回答一致性
    ),
)