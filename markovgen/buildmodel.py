##
# Reads from stdin, builds a Markov model and saves it to disk. Expected format from stdin is lines of sentences.
##

import argparse
import common
import logging
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Generates a Markov model from stdin and saves it to disk.")
    parser.add_argument("-o","--output_fn", help="Output filename for generated model", required=True)
    parser.add_argument("-n","--n_grams", help="Number of n-grams to use in model", default=2) # TODO parse as an integer
    return vars(parser.parse_args())

def tokenize_line(line):
    # TODO punctuation, normalization, blah
    return [common.START_TOK] + line.split() + [common.END_TOK]

def build_model(args):
    ngrams = args["n_grams"]

    # if ngrams is 3, we're actually building a unigram, bigram, and trigram model, not just the latter
    model = dict( (i, {}) for i in xrange(1, ngrams+1) )

    for line in sys.stdin:
        tokens = tokenize_line(line)
        logging.debug("Tokens: %s" % (tokens,))
        for i, token in enumerate(tokens):
            # foreach model, generate the necessary n-grams that led to this token
            logging.debug("i=%d: %s" % (i, token))
            for n in xrange(1, ngrams+1):
                logging.debug("\t%s" % n)
                if i >= n: # enough to support model
                    model_key = tuple(tokens[i-n:i])
                    logging.debug("\t\t%s: %s" % (model_key, token))
                    # keep track of how many times these n characters leading up to this token happens
                    # TODO perhaps this can be cleaner with defaultdicts
                    model[n].setdefault(model_key, {})
                    model[n][model_key][token] = model[n][model_key].get(token, 0) + 1

    return model

def main():
    common.configure_logging()
    args = parse_args()
    model = build_model(args)

    common.dump_model(model, args["output_fn"])

if __name__ == "__main__":
    main()
