from transformers import AutoModel, AutoTokenizer


class TokenAttentionLevelExtractor:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def agg(self, x, y, agg_method: str) -> float:
        if agg_method == 'average':
            return (x + y) / 2
        elif agg_method == 'max':
            return max(x, y)

    def get_top_bigrams_by_token_attention(self, text: str, top_k=5, token_agg_method='average'):
        inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
        outputs = self.model(**inputs, output_attentions=True)
        attention = outputs.encoder_attentions[-1].mean(dim=1).squeeze()
        tokens = self.tokenizer.tokenize(self.tokenizer.decode(inputs["input_ids"].squeeze()))
        tokens = [token for token in tokens if token not in ["</s>", "<s>", "en_XX"]]

        bigram_attention_scores = {}
        for i in range(len(tokens) - 1):
            bigram = (tokens[i], tokens[i + 1])
            attention_score = self.agg(
                attention[i, i + 1].item(),
                attention[i + 1, i].item(),
                token_agg_method,
            )
            bigram_attention_scores[bigram] = (round(attention_score, 3), i, i + 1)

        top_bigrams = sorted(
            bigram_attention_scores.items(), key=lambda x: x[1], reverse=True
        )[:top_k]

        return top_bigrams, tokens


class BigramExpander:
    def __init__(self, tokens):
        self.tokens = tokens

    def expand_token_left(self, idx):
        """
        Находит полное слово, двигаясь влево от заданного индекса.
        """
        if self.tokens[idx].startswith("▁"):
            return self.tokens[idx].strip("▁")

        parts = []
        while idx >= 0 and not self.tokens[idx].startswith("▁"):
            parts.append(self.tokens[idx].strip("▁"))
            idx -= 1
        if idx >= 0:
            parts.append(self.tokens[idx].strip("▁"))

        return "".join(reversed(parts))

    def expand_token_right(self, idx):
        """
        Находит полное слово, двигаясь вправо от заданного индекса.
        """
        parts = [self.tokens[idx].strip("▁")]
        idx += 1
        while idx < len(self.tokens) and not self.tokens[idx].startswith("▁"):
            parts.append(self.tokens[idx].strip("▁"))
            idx += 1
        return "".join(parts)

    def expand_bigrams(self, bigrams):
        bigrams_full_words = []
        for bigram, (attention, idx1, idx2) in bigrams:
            full_word1 = self.expand_token_left(idx1)
            full_word2 = self.expand_token_right(idx2
                                                 )
            word_space_sep = " " if bigram[1].startswith("▁") else ""
            bigrams_full_words.append((f"{full_word1}{word_space_sep}{full_word2}", attention))

        return bigrams_full_words
