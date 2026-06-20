# Using Perplexity Focus Modes in GXP

Perplexity offers different Focus modes that change how it approaches research. Using the right mode strategically can significantly improve the quality of research you feed into the GXP workflow.

## Recommended Focus Modes by Research Type

### Web (Default)
**Best for:**
- General technology evaluation
- Competitive landscape research
- Recent developments and news

**When to use in GXP:**
- Most Phase 0 research
- Broad context gathering

### Academic
**Best for:**
- Deep technical papers and established research
- Formal methods, algorithms, and theoretical foundations
- Areas where you want peer-reviewed sources

**When to use in GXP:**
- Evaluating new paradigms or fundamental approaches
- Researching complex distributed systems, cryptography, or specialized domains
- When you need high-trust sources for architectural decisions

### Writing
**Best for:**
- Synthesizing research into clear, well-structured narratives
- Turning scattered findings into coherent arguments

**When to use in GXP:**
- After doing initial research, when you need to synthesize findings into the **Context** section of a task brief
- Preparing research handoff documents

### Wolfram (Math & Data)
**Best for:**
- Anything involving calculations, data analysis, or symbolic reasoning

**When to use in GXP:**
- Performance modeling
- Cost estimation
- Algorithmic complexity analysis
- Any research that requires precise quantitative thinking

## Strategic Usage Pattern

A powerful pattern is to use multiple Focus modes in sequence:

1. Start with **Web** for broad discovery.
2. Switch to **Academic** when you need deeper, more rigorous sources on specific sub-topics.
3. Use **Writing** mode to help synthesize everything into clean, brief-ready language.

## Pro Tips

- You can change Focus mid-conversation. This is very useful when shifting from discovery to synthesis.
- For technical architecture research, a common powerful flow is:
  - Web → Academic → Writing
- Always note which Focus mode you used when capturing research, as it affects the character and trustworthiness of the output.

## Example Prompt with Focus Mode in Mind

When using Academic focus:

```
Using rigorous academic and peer-reviewed sources from the last 5 years, compare the consistency models and trade-offs of [System A] vs [System B] for a globally distributed application with strong latency requirements.
```

This is much more effective than using the default Web focus for the same question.