from pinecone import Pinecone
from openai import OpenAI
import numpy as np
from abc import abstractmethod, ABC
from vectorspace_driver.driver import VectorspaceDriver

PINECONE_API_KEY = "e4d3c997-d68d-4f03-a42a-6c60c6dd9b02"
OPENAI_API_KEY = "[YOUR KEY HERE]"
RES_FILE = "out.txt"

class VectorspaceInserter():
    def __init__(self, driver: VectorspaceDriver):
        self.driver = driver
        self.features = []

    def add_feature(self, feature_id, text):
        self.driver.
        



    pc_client = Pinecone(api_key=PINECONE_API_KEY)
    pc_index = pc_client.Index("test")

    openai_client = OpenAI(api_key=OPENAI_API_KEY)


    def get_embedding(text, model="text-embedding-3-small"):
        return np.array(
            openai_client.embeddings.create(input=[text], model=model).data[0].embedding
        )

    cases = {
        "openai": "OpenAI focuses on developing and deploying AI technologies, emphasizing machine learning models that can understand, generate, and translate human-like text for a wide range of applications, aiming to ensure such technologies are used ethically and to benefit society.",
        "stability": "Stability AI's primary focus is on creating advanced machine learning models capable of processing and generating content across various media types, including images, audio, and text, aiming to facilitate creative and analytical tasks through technology.",
        "grammarly": "Grammarly's primary purpose is to provide AI-powered writing assistance, focusing on improving grammar, spelling, punctuation, clarity, engagement, and delivery in English texts, tailored for various platforms including web, desktop, and mobile applications.",
        "runaway": "Runway focuses on advancing AI research to develop tools that enhance creative processes across art, entertainment, and storytelling, facilitating the generation of videos, images, and custom AI models through an accessible platform.",
        "webflow": "Webflow enables users to design, build, and launch responsive websites visually, without writing code, by providing a visual editor that translates design choices into HTML, CSS, and JavaScript, offering advanced design, animation, and content management features.",
        "wix": "Wix.com provides a platform for building websites through a visual editor that allows users to design and customize their web presence without the need for coding, offering a range of templates, e-commerce solutions, and SEO tools to support various types of online projects and businesses.",
        "react": "React.dev focuses on providing a JavaScript library for building user interfaces, particularly for web and native platforms, enabling developers to create reusable UI components that manage state and handle updates dynamically for interactive applications.",
        "angular": "Angular.io is dedicated to offering a platform for building mobile and desktop web applications, utilizing a TypeScript-based open-source framework designed to make the development and testing process more efficient by providing a structured environment for building dynamic and complex applications.",
        "wordpress": "WordPress.org is dedicated to providing a flexible and open-source content management system (CMS) that enables users to create and manage websites through a wide variety of themes, plugins, and customizable options, focusing on ease of use for publishing content and creating webpages without needing to code."
    }

    vectors = []
    for key, sent in cases.items():
        emb = get_embedding(sent)
        vectors.append({"id": key, "values": emb})
    pc_index.upsert(vectors=vectors, namespace="poc")
