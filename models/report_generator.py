import os
from groq import Groq

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    if not os.environ.get("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY environment variable not found.")
        client = None
    else:
        print("✅ Groq client initialized successfully.")
except Exception as e:
    print(f"ERROR: Could not initialize Groq client: {e}")
    client = None

def write_report(rag_context: str, observations: str, results: str) -> str:
    if not client:
        return ("Error: Groq API client is not initialized. "
                "Please ensure your GROQ_API_KEY is set correctly in the .env file.")

    prompt = f"""
        You are a meticulous scientific assistant. Your task is to write a formal and detailed lab report using the provided information.

        ---
        ### INSTRUCTIONS
        ---
        **1. Report Structure:**
        The report MUST include the following sections, each with a clear heading:
        - Aim
        - Theory
        - Apparatus / Requirements
        - Procedure
        - Observations
        - Calculations / Results
        - Conclusion

        **2. Tone and Style:**
        - The language must be formal, objective, and appropriate for a scientific document.
        - Write in clear and complete sentences. Avoid overly simplistic or fragmented language.
        - Ensure smooth transitions between sections to create a cohesive document.

        **3. Data Handling:**
        - Accurately present all data from the 'USER-PROVIDED OBSERVATIONS' and 'CALCULATED RESULTS' sections.
        - If 'USER-PROVIDED OBSERVATIONS' are missing or incomplete, generate realistic sample readings consistent with the experiment's context.
        - If 'CALCULATED RESULTS' are missing or contain an error message, generate appropriate sample calculations and results based on the observations.

        **4. Formatting:**
        - The final response must be in plain text format only. Do not use markdown or emojis.

        ---
        ### EXAMPLE OF HIGH-QUALITY OUTPUT STYLE
        ---
        Here is an example of a well-written conclusion to guide your writing style:

        Conclusion: The experimental results clearly demonstrate that surface grinding produces a superior surface finish compared to face milling on mild steel. The surface grinder achieved an Ra value of 0.8 μm, which is significantly smoother than the best finish from the milling machine (2.1 μm). This outcome confirms the theoretical expectation that abrasive finishing processes yield a lower surface roughness than chip removal processes.

        ---
        **PROVIDED INFORMATION**
        ---

        **1. AIM, THEORY, and PROCEDURE (extracted from the lab manual):**
        {rag_context}

        **2. OBSERVATIONS (provided by the user):**
        {observations}

        **3. CALCULATED RESULTS (from the executed Python code):**
        {results}

        ---
        **END OF INFORMATION**
        ---

        Now, please generate the complete lab report.
        """
        
    print("Sending request to Groq API...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile", 
            temperature=1.0,       
            max_tokens=2048,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"ERROR: An error occurred while calling the Groq API: {e}")
        return f"An error occurred while generating the report: {e}"