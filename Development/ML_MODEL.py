{
#all installs
# !pip install -q -U trl transformers accelerate git+https://github.com/huggingface/peft.git
# !pip install -q datasets bitsandbytes einops wandb
# !pip install huggingface_hub

#all imports
# import time
# from huggingface_hub import notebook_login
# from transformers import TrainingArguments
# from trl import SFTTrainer

# from datasets import load_dataset
# !huggingface-cli login
}
import torch
from peft import PeftConfig, PeftModel
import re
from typing import List
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_community.llms import HuggingFacePipeline
from langchain.schema import BaseOutputParser
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain.chains.conversation.memory import ConversationBufferMemory
import warnings
import os
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    StoppingCriteria,
    StoppingCriteriaList,
    # GenerationConfig,
    pipeline)
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)

# Set environment variable to turn off oneDNN custom operations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


class Model():
    def __init__(self):
      self.falcon_model = None
      self.falcon_model_peft = None
      self.falcon_tokenizer = None
      self.gen_config = None
      self.chain = None
    #-------------------------------------------------------------------------------------------------------------------------------------
    def load_pretrained(self):
        # Creates an instance of BitsAndBytesConfig with specific settings for quantization.

        # BitsAndBytesConfig for quantization settings
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            # bnb_4bit_quant_type="nf4",
            # bnb_4bit_use_double_quant=True,
            # bnb_4bit_compute_dtype=torch.float16,
            # llm_int8_enable_fp32_cpu_offload=True
        )

        # Load and configure the Falcon model and tokenizer
        config = AutoModelForCausalLM.from_pretrained("MODEL_FILES")
        self.falcon_model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            return_dict=True,
            quantization_config=bnb_config,
            # low_cpu_mem_usage = True,
            trust_remote_code=True,
            device_map="cuda:0"
        )
        #-----------------------------------------------------------------------------------------
        self.falcon_tokenizer = AutoTokenizer.from_pretrained(
            config.base_model_name_or_path,
            trust_remote_code=True
        )
        self.falcon_tokenizer.pad_token = self.falcon_tokenizer.eos_token
        #-----------------------------------------------------------------------------------------
        self.falcon_model_peft = PeftModel.from_pretrained(self.falcon_model,"MODEL_FILES")

        # # set teh generation configuration params
        self.gen_config = self.falcon_model_peft.generation_config
        self.gen_config.max_new_tokens = 100
        self.gen_config.temperature = 0.4
        self.gen_config.top_p = 0.4
        self.gen_config.num_return_sequences = 1
        self.gen_config.repetition_penalty= 1.7
        self.gen_config.pad_token_id = self.falcon_tokenizer.pad_token_id
        self.gen_config.eos_token_id = self.falcon_tokenizer.eos_token_id

        self.Create_Chain()
    
    def Create_Chain(self):

        generation_pipeline = pipeline(
            model=self.falcon_model_peft,
            tokenizer=self.falcon_tokenizer,
            return_full_text=True,
            task="text-generation",
            # stopping_criteria=stopping_criteria,
            generation_config=self.gen_config,
            do_sample = False,
            use_cache = True
        )

        llm = HuggingFacePipeline(pipeline=generation_pipeline)
        template = """
        You're a psychologist, and a patient has reached out to you for help.\n\n{history}\n\npatient: {input}\npsychologist:""".strip()

        prompt = PromptTemplate(input_variables=["history","input"], template=template)
        
        # memory = ConversationBufferMemory()
        # memory = ConversationSummaryMemory(llm=self.llm)

        # We set a low k=2, to only keep the last 2 interactions in memory
        memory = ConversationBufferWindowMemory(
            memory_key="history", k=4, return_only_outputs=True
        )

        self.chain = ConversationChain(
            llm=llm,
            memory = memory,
            prompt=prompt,
            # output_parser=self.LastWordFinder(),
            verbose=True,
        )
    #-------------------------------------------------------------------------------------------------------------------------------------
    def get_last_psychologist_response(self, conversation):
        """
        This function takes a conversation string and returns the last response from the psychologist,
        without the "psychologist:" prefix.
        
        Parameters:
        conversation (str): The full conversation as a string.
        
        Returns:
        str: The last response from the psychologist without the prefix.
        """
        # Split the conversation into lines
        lines = conversation.split('\n')
        
        # Initialize variables to track the last psychologist response
        last_psychologist_response = []
        current_response = []
        is_psychologist = False
        
        # Iterate through the lines to find and capture the psychologist's responses
        for line in lines:
            if line.startswith('psychologist:'):
                if current_response:
                    last_psychologist_response = current_response
                    current_response = []
                is_psychologist = True
                # Append the line without the "psychologist:" prefix
                current_response.append(line[len('psychologist:'):].strip())
            elif line.startswith('patient:'):
                is_psychologist = False
            
            elif is_psychologist:
                current_response.append(line)
        
        # Capture the last response after the loop
        if current_response:
            last_psychologist_response = current_response
        
        # Join the lines of the last psychologist response
        return '\n'.join(last_psychologist_response)
    #-------------------------------------------------------------------------------------------------------------------------------------
    def Chain(self,text):
        conv  = self.chain.predict(input=text)
        return self.get_last_psychologist_response(conv)
    #-------------------------------------------------------------------------------------------------------------------------------------
    def get_response_falcon(self,input):
        template = """
        You're a psychologist, and a patient has reached out to you for help.\n\n\npatient: {input}\npsychologist:""".strip()
        prompt = template.format(input=input)

        falcon_encoding = self.falcon_tokenizer(prompt, return_tensors="pt").to(self.falcon_model.device)

        with torch.inference_mode():
            falcon_outputs = self.falcon_model_peft.generate(
                input_ids = falcon_encoding.input_ids,
                attention_mask = falcon_encoding.attention_mask,
                generation_config = self.gen_config
            )

        falcon_text_output = self.falcon_tokenizer.decode(falcon_outputs[0].cuda(), skip_special_tokens=True)
        return  falcon_text_output
    #-------------------------------------------------------------------------------------------------------------------------------------
    def generate_answer(self,query):
        # system_prompt = """Answer the following question truthfully.
        # If you don't know the answer, respond 'Sorry, I don't know the answer to this question.'.
        # If the question is too complex, respond 'Kindly, consult a psychiatrist for further queries.'."""
        system_prompt = """You are a psychotherapist for people seeking help to improve their mental health.
        The patient expects 5 sentences from you . talk about the disease , effects of this disease , advice to the patient , suggest medicine to the patient ,  how can to be better ?
        """

        user_prompt = f"""<patient>: {query}
        <therapist>: """

        final_prompt = system_prompt + "\n" + user_prompt
        device = "cuda:0"

        peft_encoding = self.falcon_tokenizer(final_prompt, return_tensors="pt").to(device)
        peft_outputs = self.falcon_model.generate(input_ids=peft_encoding.input_ids, generation_config=self.gen_config)  # Add stopping criteria
        peft_text_output = self.falcon_tokenizer.decode(peft_outputs[0], skip_special_tokens=True)
        return peft_text_output
    

model = Model()
model.load_pretrained()
generated_text = model.generate_answer("I've been having flashbacks and nightmares about a traumatic event. What is happening to me? ")
print(generated_text)

