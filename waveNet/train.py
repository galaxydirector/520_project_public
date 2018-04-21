# This file serves the purpose of train models.


path = "../Project/words/"
words = os.listdir(path)

dict_words = {}

for word in words:
    dict_words[word] = np.loadtxt(path+word, delimiter = ",")
# Divide into feature matrix and label vector
dict_X = {}
dict_Y = {}
for word in words:
    dict_X[word] = dict_words[word][:,:-1]
    dict_Y[word] = dict_words[word][:,-1] 
# load data
train_data =
test_data =

output_classes = 

# training params
initialize = True
iteration_start = 0

# model params
params = {
	'batch_size':1,
    'dilations':[1,2,1,2],
    'filter_width':2,
    'residual_filters':8,
    'dilation_filters':8,
    'skip_filters':32,
    'input_channels':100,
    'output_classes': ,
    'use_biases': False,
    'global_condition_channels': None,
    'global_condition_cardinality': None
}






initializer = tf.global_variables_initializer()
saver = tf.train.Saver(max_to_keep = 10)

with tf.Session() as sess:
    
    if initialize:
        sess.run(initializer)
    else:
        ckpt_file = './models/params_' + str(iteration_start) + '.ckpt'
        print('restoring parameters from', ckpt_file)
        print("Model restored.")
        saver.restore(sess, ckpt_file)

    # create log writer object
    logs_path = './train_logs/logs'
    train_writer = tf.summary.FileWriter(logs_path, graph=tf.get_default_graph())
    # train_writer = tf.summary.FileWriter(logs_path, graph=sess.graph)
    # train_writer.add_graph(sess.graph)


    print(sess.run(w1))
    print(sess.run(w2))
    
    for i in range(iteration_start, steps): ##################

        #选定每一个批量读取的首尾位置，确保在1个epoch内采样训练
        start = i * batch_size % data_size
        end = min(start + batch_size,data_size)
        _, summary = sess.run([train_step,summary_op],feed_dict={x:X[start:end],y:Y[start:end]})
        # writer.add_summary(summary, epoch * batch_count + i)
        train_writer.add_summary(summary, i)
        if i % 1000 == 0:
            training_loss= sess.run(cross_entropy,feed_dict={x:X,y:Y})
            print("By %d iteration，Training loss is %g"%(i,training_loss))
            # save the model
            saver.save(sess, './models/params_' + str(i) + '.ckpt')