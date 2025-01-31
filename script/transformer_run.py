from transformer.model.transformer_encoder import TransformerEncoder
from transformer.model.transformer_decoder import TransformerDecoder
from transformer import transformer_hyperparas
from transformer.test.transformer_predict_beam import transformer_predict_beam
from transformer.test.predict_greedy import predict_greedy
from str_process import stl_template_extractor
from str_process import string_accuracy
from str_process import bleu
from str_process import eng_split
from str_process import stl_compact
from public import paths
import torch
from d2l import torch as d2l
import pickle
import time
import json
import sys


# IMPORTANT SETTINGS
# predictor - 'greedy' (greedy search)
#           - 'beam'   (beam search)
predictor = 'beam'
# the folder name where data is stored
seed_list = [100]
# mode - 'inner_test'
#      - 'extrapolate'
#      - 'output_results'
mode_list = ['json']

# transformer paras
key_size = query_size = value_size = num_hiddens = transformer_hyperparas.num_hiddens
norm_shape = [num_hiddens]
ffn_num_input, ffn_num_hiddens = transformer_hyperparas.num_hiddens, transformer_hyperparas.ffn_num_hiddens
num_layers, num_heads = transformer_hyperparas.num_layers, transformer_hyperparas.num_heads
dropout = transformer_hyperparas.dropout_rate

# dataset & tokenizer & vocabulary
f = open(paths.preprocess_info_dict_path, 'rb')
preprocess_info_dict = pickle.load(f)
f.close()
src_vocab = preprocess_info_dict['eng_tokenizer']
tgt_vocab = preprocess_info_dict['stl_tokenizer']
len_src_vocab = src_vocab.get_vocab_size()
len_tgt_vocab = tgt_vocab.get_vocab_size()
num_steps = preprocess_info_dict['max_length']

# device
device = transformer_hyperparas.device

# define model
encoder = TransformerEncoder(len_src_vocab, key_size, query_size, value_size,
                             num_hiddens, norm_shape, ffn_num_input,
                             ffn_num_hiddens, num_heads, num_layers, dropout)
decoder = TransformerDecoder(len_tgt_vocab, key_size, query_size, value_size,
                             num_hiddens, norm_shape, ffn_num_input,
                             ffn_num_hiddens, num_heads, num_layers, dropout)
net = d2l.EncoderDecoder(encoder, decoder)


def output_json(net, src_vocab, tgt_vocab, num_steps, device, spec_path, tl_path):
    f = open(spec_path)
    data = json.load(f)

    tls_f = open(tl_path, "w")
    tls = {"temporal_logic_formulars" : []}

    for sentence_entry in data:
        specification = sentence_entry["sentence"]
        src_sentence = eng_split.split_identifier(specification)
        if predictor == 'greedy':
            pred_id_list, pred, attention_weight = \
                predict_greedy(net, src_sentence, src_vocab, tgt_vocab, num_steps, device)
        else:
            pred_id_list, pred, criterion, attention_weight = \
                transformer_predict_beam(net, src_sentence, src_vocab, tgt_vocab, num_steps, device)
        result = stl_compact.delete_stl_id_num_space(pred)
        tl_entry = {**sentence_entry, "tl":result}
        tls["temporal_logic_formulars"].append(tl_entry)

    print("Complete! Output Json")
    json.dump(tls, tls_f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    for seed in seed_list:
        print('seed:', seed)
        if len(sys.argv) != 3:
            print("Usage: python script.py <file1> <file2>")
            sys.exit(1)

        # The first argument is the script name, so we start from index 1
        spec_path = sys.argv[1]
        tl_path = sys.argv[2]

        if device != torch.device('cpu'):
            net.load_state_dict(torch.load(paths.transformer_record_path + str(seed) + '/net_state_dict'))
            net.to(device)
        else:  # cpu is used
            net.load_state_dict(torch.load(paths.transformer_record_path + str(seed) + '/net_state_dict',
                                           map_location=torch.device('cpu')))

        output_json(net, src_vocab, tgt_vocab, num_steps, device, spec_path, tl_path)
        print()
