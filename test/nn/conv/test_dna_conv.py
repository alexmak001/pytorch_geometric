import torch
from torch_geometric.nn import DNAConv


def test_dna_conv():
    channels = 32
    num_layers = 3
    edge_index = torch.tensor([[0, 0, 0, 1, 2, 3], [1, 2, 3, 0, 0, 0]])
    num_nodes = edge_index.max().item() + 1
    x = torch.randn((num_nodes, num_layers, channels))

    conv = DNAConv(channels, heads=4, groups=8, dropout=0.0)
    assert conv.__repr__() == 'DNAConv(32, heads=4, groups=8)'
    out = conv(x, edge_index)
    assert out.size() == (num_nodes, channels)

    jit_conv = conv.jittable(x=x, edge_index=edge_index)
    jit_conv = torch.jit.script(jit_conv)
    assert jit_conv(x, edge_index).tolist() == out.tolist()

    conv = DNAConv(channels, heads=1, groups=1, dropout=0.0)
    assert conv.__repr__() == 'DNAConv(32, heads=1, groups=1)'
    out = conv(x, edge_index)
    assert out.size() == (num_nodes, channels)

    jit_conv = conv.jittable(x=x, edge_index=edge_index)
    jit_conv = torch.jit.script(jit_conv)
    assert jit_conv(x, edge_index).tolist() == out.tolist()

    conv = DNAConv(channels, heads=1, groups=1, dropout=0.0, cached=True)
    out = conv(x, edge_index)
    out = conv(x, edge_index)
    assert out.size() == (num_nodes, channels)

    jit_conv = conv.jittable(x=x, edge_index=edge_index)
    jit_conv = torch.jit.script(jit_conv)
    jit_conv(x, edge_index)
    assert jit_conv(x, edge_index).tolist() == out.tolist()
