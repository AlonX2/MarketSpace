from feature_extractor.prompt_generator import PromptGeneratorA
from feature_extractor.llm_client import GPTClient
from feature_extractor.main import FeatureResolver
from product.product import Product

fr = FeatureResolver(prompt_generator=PromptGeneratorA(), llm_client=GPTClient())
p = Product("a", "wix", "https://www.wix.com/", features=dict())
ps = [p]
ps = fr.resolve_features(ps)

print(ps)