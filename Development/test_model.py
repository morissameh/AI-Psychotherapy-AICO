from transformers import pipeline, GenerationConfig, AutoTokenizer, AutoModelForCausalLM

class PsychotherapistAssistant:

    def __init__(self):

        self.tokenizer = AutoTokenizer.from_pretrained("moris12345/falcon-moris-2", trust_remote_code=True)
        # self.model = AutoModelForCausalLM.from_pretrained("moris12345/falcon-moris-2", trust_remote_code=True)

        # Create generation config for prediction
        self.generation_config = GenerationConfig.from_pretrained("moris12345/falcon-moris-2", trust_remote_code=True)
        self.generation_config.max_new_tokens = 100
        self.generation_config.temperature = 0.4
        self.generation_config.top_p = 0.4
        self.generation_config.repetition_penalty = 1.7
        self.generation_config.num_return_sequences = 1
        self.generation_config.pad_token_id = self.tokenizer.pad_token_id
        self.generation_config.eos_token_id = self.tokenizer.eos_token_id

        # Initialize the text-generation pipeline with the model and tokenizer
        self.pipe = pipeline("text-generation", model="moris12345/falcon-moris-2", max_new_tokens=100, temperature=0.4, top_p=0.4, repetition_penalty=1.7, num_return_sequences=1)

    def generate_answer(self, query):
        system_prompt = """You are a psychotherapist for people seeking help to improve their mental health.
        The patient expects 5 sentences from you: talk about the disease, effects of this disease, advice to the patient, suggest medicine to the patient, and how to be better.
        """

        user_prompt = f"""<patient>: {query}
        <therapist>: """

        final_prompt = system_prompt + "\n" + user_prompt

        # Use the pipeline to generate the response
        response = self.pipe(final_prompt, max_length=100, num_return_sequences=1)

        return response

# Example usage
assistant = PsychotherapistAssistant()
query = "I've been having flashbacks and nightmares about a traumatic event. What is happening to me?"
response = assistant.generate_answer(query)
print(response)
