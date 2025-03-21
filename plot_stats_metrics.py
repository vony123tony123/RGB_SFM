
from torchsummary import summary
from torch import nn
import torch

from loss.loss_function import get_loss_function
from models.SFMCNN import SFMCNN
from models.RGB_SFMCNN import RGB_SFMCNN
from models.RGB_SFMCNN_V2 import RGB_SFMCNN_V2
from dataloader import get_dataloader
from config import *


from monitor.monitor_method import get_all_layers_stats
from monitor.plot_df import json_to_table, save_table_as_image, plot_heatmap
from monitor.plot_monitor import plot_all_layers_graph

with torch.no_grad():
    # Load Dataset
    train_dataloader, test_dataloader = get_dataloader(dataset=config['dataset'], root=config['root'] + '/data/',
                                                       batch_size=config['batch_size'],
                                                       input_size=config['input_shape'])
    images, labels = torch.tensor([]), torch.tensor([])
    for batch in test_dataloader:
        imgs, lbls = batch
        images = torch.cat((images, imgs))
        labels = torch.cat((labels, lbls))
    print(images.shape, labels.shape)

    # Load Model
    models = {'SFMCNN': SFMCNN, 'RGB_SFMCNN': RGB_SFMCNN, 'RGB_SFMCNN_V2': RGB_SFMCNN_V2}
    checkpoint_filename = 'RGB_SFMCNN_V2_best'
    checkpoint = torch.load(f'./pth/{config["dataset"]}_pth/{checkpoint_filename}.pth', weights_only=True)
    model = models[arch['name']](**dict(config['model']['args']))
    model.load_state_dict(checkpoint['model_weights'])
    model.cpu()
    model.eval()
    summary(model, input_size=(config['model']['args']['in_channels'], *config['input_shape']), device='cpu')
    print(model)

    # Test Model
    batch_num = 1000
    pred = model(images[:batch_num])
    y = labels[:batch_num]
    correct = (pred.argmax(1) == y.argmax(1)).type(torch.float).sum().item()
    print("Test Accuracy: " + str(correct / len(pred)))

    loss_fn = get_loss_function(config['loss_fn'])
    loss = loss_fn(pred, y)
    # input()

layers = get_layers(model)
layers_infos = config['layers_infos']
# print(layers)
# print(layers_infos)


layer_stats, overall_stats = get_all_layers_stats(model, layers, layers_infos, images)

save_path = f'./detect/{config["dataset"]}_{checkpoint_filename}/RM_monitor'

# 確保保存目錄存在
os.makedirs(save_path, exist_ok=True)

# Convert to table
df = json_to_table(layer_stats, overall_stats )
print(df)

save_table_as_image(df, save_path + "/layers_table.png", title="Layer Metrics Table")
plot_heatmap(df, save_path + "/heat_map.png", title="Layer Metrics Table")

plot_all_layers_graph(model, layers, layers_infos, images, save_path, space_count=10)