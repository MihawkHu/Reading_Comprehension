import theano
import theano.tensor as T
import lasagne
import lasagne.layers as L
import numpy as np

def Tconcat(t1,t2):
    return T.concatenate([t1,t2], axis=2)

def Tsum(t1,t2):
    return t1+t2

class GatedAttentionLayer(L.MergeLayer):
    def __init__(self, incomings, gating_fn='T.mul', mask_input=None, transpose=False, **kwargs):
        super(GatedAttentionLayer, self).__init__(incomings, **kwargs)
	self.gating_fn = gating_fn
        if mask_input is not None and type(mask_input).__name__!='TensorVariable': 
            raise TypeError('Mask input must be theano tensor variable')
        self.mask = mask_input
        self.transpose = transpose

    def get_output_shape_for(self, input_shapes):
        if self.gating_fn=='Tconcat': 
            return (input_shapes[0][0],input_shapes[0][1],input_shapes[0][2]+input_shapes[1][2])
        else:
            return input_shapes[0]

    def get_output_for(self, inputs, attention_only=False, **kwargs):
        if self.transpose: M = inputs[2].dimshuffle((0,2,1))
        else: M = inputs[2]
        alphas = T.nnet.softmax(T.reshape(M, (M.shape[0]*M.shape[1],M.shape[2])))
        alphas_r = T.reshape(alphas, (M.shape[0],M.shape[1],M.shape[2]))* \
                self.mask[:,np.newaxis,:] # B x N x Q
        alphas_r = alphas_r/alphas_r.sum(axis=2)[:,:,np.newaxis] # B x N x Q
        q_rep = T.batched_dot(alphas_r, inputs[1]) # B x N x D
    
        return eval(self.gating_fn)(inputs[0],q_rep)

class PairwiseInteractionLayer(L.MergeLayer):
    def __init__(self, incomings, **kwargs):
        super(PairwiseInteractionLayer, self).__init__(incomings, **kwargs)

    def get_output_shape_for(self, input_shapes):
        return (input_shapes[0][0], input_shapes[0][1], input_shapes[1][1])

    def get_output_for(self, inputs, **kwargs):

        # inputs[0]: B x N x D
        # inputs[1]: B x Q x D
        # self.mask: B x Q

        q_shuf = inputs[1].dimshuffle(0,2,1) # B x D x Q
        return T.batched_dot(inputs[0], q_shuf) # B x N x Q

class AttentionSumLayer(L.MergeLayer):
    def __init__(self, incomings, aggregator, pointer, mask_input=None, **kwargs):
        super(AttentionSumLayer, self).__init__(incomings, **kwargs)
        if mask_input is not None and type(mask_input).__name__!='TensorVariable': 
            raise TypeError('Mask input must be theano tensor variable')
        self.mask = mask_input
        self.aggregator = aggregator
        self.pointer = pointer
        
    def get_output_shape_for(self, input_shapes):
        return (input_shapes[2][0], input_shapes[2][2])

    def get_output_for(self, inputs, **kwargs):
        q = inputs[1][T.arange(inputs[1].shape[0]),self.pointer,:] # B x D
        p = T.batched_dot(inputs[0],q) # B x N
        pm = T.nnet.softmax(p)*self.mask # B x N
        pm = pm/pm.sum(axis=1)[:,np.newaxis] # B x N

        return T.batched_dot(pm, self.aggregator)

class BilinearAttentionLayer(L.MergeLayer):
    def __init__(self, incomings, num_units, W=lasagne.init.Uniform(), 
            mask_input=None, **kwargs):
        super(BilinearAttentionLayer, self).__init__(incomings, **kwargs)
        self.num_units = num_units
        if mask_input is not None and type(mask_input).__name__!='TensorVariable': 
            raise TypeError('Mask input must be theano tensor variable')
        self.mask = mask_input
        self.W = self.add_param(W, (num_units, num_units), name='W')

    def get_output_shape_for(self, input_shapes):
        return (input_shapes[0][0], input_shapes[0][2])

    def get_output_for(self, inputs, **kwargs):
        qW = T.dot(inputs[1], self.W) # B x H
        qWp = (inputs[0]*qW[:,np.newaxis,:]).sum(axis=2)
        alphas = T.nnet.softmax(qWp)
        if self.mask is not None:
            alphas = alphas*self.mask
            alphas = alphas/alphas.sum(axis=1)[:,np.newaxis]
        return (inputs[0]*alphas[:,:,np.newaxis]).sum(axis=1)

class IndexLayer(L.MergeLayer):
    def get_output_shape_for(self, input_shapes):
        return input_shapes[0] + (input_shapes[1][-1],)

    def get_output_for(self, inputs, **kwargs):
        return inputs[1][inputs[0]]

