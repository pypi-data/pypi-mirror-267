# Models

### Model Params
```markdown
"model_params": {
    "temperature": float,
    "max_tokens": int,
    "top_p": float,
    "top_k": int,
},
"enable_search": bool,
"search_params": {
    "collection": "asu",
    "top_k": int,
}
```
#### temperature
Randomness and Diversity parameter. Use a lower value to decrease randomness in the response.
#### top_p
Randomness and Diversity parameter. Use a lower value to ignore less probable options.
#### top_k
Randomness and Diversity parameter. The number of token choices the model uses to generate the next token.
#### max_tokens
The maximum number of tokens in the generated response.

## Provider: AES
Checkout [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html) for base model ids and versions.

### Titan Text Models

Model IDs:
- titang1lite
- titang1express

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html):

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 1       |
| Length                   | max_tokens  | max_tokens  | 0       | 8000    | 512     |


### Anthropic Claude models

Model IDs:
- claude2_1 
- claude2 
- claude1_3 
- claudeinstant

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html):

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.5     |
| Randomness and diversity | Top K       | top_k       | 0       | 500     | 250     |
| Length                   | max_tokens  | max_tokens  | 0       | 4096    | 200     |

### AI21 Labs Jurassic-2 models

Model IDs:
- j2ultra
- j2mid

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-jurassic2.html)

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.5     |
| Length                   | max_tokens  | max_tokens  | 0       | 8191    | 200     |

### Cohere Command Models

Model IDs:
- command
- commandlight

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 5       | 0.9     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.75    |
| Randomness and diversity | Top K       | top_k       | 0       | 500     | 0       |
| Length                   | max_tokens  | max_tokens  | 1       | 4096    | 20      |

### Meta Llama2 Models

Model IDs:
- llama2-13b

[Model Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html)

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.9     |
| Length                   | max_tokens  | max_tokens  | 1       | 2048    | 512     |


## Provider: Azure

[Model Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)

| Model name | Model ID         | Max Request (tokens) |
|------------|------------------|----------------------|
| gpt3_5     | gpt-35-turbo     | 4096                 |
| gpt3_5-16k | gpt-35-turbo-16k | 16384                |
| gpt4       | gpt-4            | 8192                 |
| gpt4-32k   | gpt-4-32k        | 32768                |

## Provider: GCP

[Model Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models)

| Model name          | Model ID       | Max Input Tokens     | Max Output Tokens |
|---------------------|----------------|----------------------|-------------------|
| PaLM 2 for Chat     | chat-bison     | 8192                 | 1024              |
| PaLM 2 for Chat 32k | chat-bison-32k | 32768 (input+output) | 8192              |
