import os
from dotenv import load_dotenv

load_dotenv()


class LLMBuilder:
    def __init__(self, temperature: float, model_override: str = None):
        if temperature is None:
            raise ValueError("Debes especificar la temperatura al instanciar LLMBuilder")

        self.provider = os.getenv("LLM_PROVIDER", "GROQ").upper()
        self.temperature = float(temperature)
        self.model_override = model_override
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        if self.provider == "GROQ":
            from langchain_groq import ChatGroq
            model = self.model_override or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            # max_tokens debe ser menor que el límite TPM de Groq (6000 plan gratuito)
            # Para el router usamos 50, para agentes 2000
            max_tok = 50 if "instant" in model else 2000
            return ChatGroq(
                model=model,
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=self.temperature,
                max_tokens=max_tok,
            )

        elif self.provider == "OPENAI":
            from langchain_openai import AzureChatOpenAI
            return AzureChatOpenAI(
                azure_deployment=os.getenv("OPENAI_DEPLOYMENT"),
                temperature=self.temperature,
                azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
                api_key=os.getenv("OPENAI_API_KEY"),
                api_version=os.getenv("OPENAI_API_VERSION"),
                max_tokens=4096,
            )

        elif self.provider == "GOOGLE":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=os.getenv("GOOGLE_MODEL", "gemini-1.5-flash"),
                api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=self.temperature,
                max_output_tokens=4096,
            )

        else:
            raise ValueError("LLM_PROVIDER debe ser GROQ, OPENAI o GOOGLE")

    def invoke(self, prompt, **kwargs):
        response = self.llm.invoke(prompt, **kwargs)

        if isinstance(response.content, str):
            clean_text = response.content
        elif isinstance(response.content, list):
            clean_text = "".join(
                block.get("text", "") for block in response.content
            )
        else:
            clean_text = str(response.content)

        response.content = clean_text
        return response