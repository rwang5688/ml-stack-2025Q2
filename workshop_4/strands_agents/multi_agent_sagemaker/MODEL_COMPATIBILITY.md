# SageMaker Model Compatibility for Strands Agents

## Critical Issue: Model Selection Matters

**This issue cost significant development time and should be clearly documented.**

## The Problem

When using SageMaker models with Strands Agents, you'll encounter this error with incompatible models:

```
ModelError: Received client error (422) from primary with message 
"{"error":"Template error: template not found","error_type":"template_error"}"
```

## Root Cause

**Model Compatibility:**
The SageMaker provider is designed to work with models that support OpenAI-compatible chat completion APIs. During development and testing, the provider has been validated with Mistral-Small-24B-Instruct-2501, which demonstrated reliable performance across various conversational AI tasks.

## Compatible Models ✅

- **Mistral-Small-24B-Instruct-2501** (validated and recommended)
- **Models that support OpenAI-compatible chat completion APIs**

## Incompatible Models ❌

- **Open Llama 7b V2** (base model, no chat completion API support)
- **Other base/foundation models without OpenAI-compatible chat APIs**

## How to Verify Model Compatibility

1. Check if the model name contains "Instruct", "Chat", or similar
2. Look for chat template configuration in the model's tokenizer config
3. Test with a simple agent call - compatible models won't throw template errors

## Official Documentation

Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/sagemaker/

## Important Note from Official Docs

> **Note: Tool calling support varies by model. Models like Mistral-Small-24B-Instruct-2501 have demonstrated reliable tool calling capabilities, but not all models deployed on SageMaker support this feature. Verify your model's capabilities before implementing tool-based workflows.**

## Recommendation

**Always use instruction-tuned models** when working with Strands Agents on SageMaker. This will save significant debugging time and ensure proper functionality.

## Time Investment Warning

⚠️ **This compatibility issue caused extensive debugging time.** Always verify model compatibility before beginning integration work.