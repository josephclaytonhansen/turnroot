from src.UI_Dialogs import textEntryDialog

def layerDown(parent):
    if parent.layers_box.currentItem() != None:
        for layer in parent.layer_orders:
            if parent.layer_orders[layer] == parent.layers_box.currentItem().text():
                tmp_layer_orders = parent.layer_orders
                tmp_images = parent.composites
                check = layer
                
        parent.layer_orders = {}
        parent.composites = {}
        try:
            if check < len(tmp_layer_orders):
                for n in tmp_layer_orders:
                    if n == check:
                        parent.layer_orders[check] = tmp_layer_orders[check+1]
                        parent.composites[check-1] = tmp_images[check]
                    elif n == check+1:
                        parent.layer_orders[check+1] = tmp_layer_orders[check]
                        parent.composites[check] = tmp_images[check-1]
                    else:
                        parent.layer_orders[n] = tmp_layer_orders[n]
                        parent.composites[n-1] = tmp_images[n-1]
                parent.layers_box.clear()
                for g in parent.layer_orders:
                    parent.layers_box.addItem(parent.layer_orders[g])
            else:
                parent.layer_orders = tmp_layer_orders
                parent.layers_box.clear()
                for g in parent.layer_orders:
                    parent.layers_box.addItem(parent.layer_orders[g])
        except Exception as e:
            pass
        try:
            parent.layers_box.setCurrentRow(check)
            parent.render()
        except:
            pass

def layerUp(parent):
    if parent.layers_box.currentItem() != None:
        for layer in parent.layer_orders:
            if parent.layer_orders[layer] == parent.layers_box.currentItem().text():
                tmp_layer_orders = parent.layer_orders
                tmp_images = parent.composites
                check = layer
                
        parent.layer_orders = {}
        parent.composites = {}
        try:
            if check > 1:
                for n in tmp_layer_orders:
                    if n == check:
                        parent.layer_orders[check] = tmp_layer_orders[check-1]
                        parent.composites[check-1] = tmp_images[check-2]
                    elif n == check-1:
                        parent.layer_orders[check-1] = tmp_layer_orders[check]
                        parent.composites[check-2] = tmp_images[check-1]
                    else:
                        parent.layer_orders[n] = tmp_layer_orders[n]
                        parent.composites[n-1] = tmp_images[n-1]
                parent.layers_box.clear()
                for g in parent.layer_orders:
                    parent.layers_box.addItem(parent.layer_orders[g])
            else:
                parent.layer_orders = tmp_layer_orders
                parent.layers_box.clear()
                for g in parent.layer_orders:
                    parent.layers_box.addItem(parent.layer_orders[g])
        except Exception as e:
            pass
        try:
            parent.layers_box.setCurrentRow(check-2)
            parent.render()
        except:
            parent.layers_box.setCurrentRow(0)
            try:
                parent.render()
            except:
                pass
            
def layerDelete(parent, layer, string):
    layer_orders = parent.layer_orders
    tmp_layer_orders = layer_orders
    layer_orders = {}
    tmp_layer_orders2 = tmp_layer_orders.copy()
    tmp_layer_orders2.pop(layer+1)
    
    layer_images = parent.composites
    tmp_layer_images = parent.composites
    layer_images = {}
    tmp_layer_images2 = tmp_layer_images.copy()
    tmp_layer_images2.pop(layer)
    
    go_to = len(tmp_layer_orders2)
    active_index = 0
    skip_index = layer+1
    
    if string.split(" ")[0] in parent.current_layer_options_container.counts:
        parent.current_layer_options_container.counts[string.split(" ")[0]] = parent.current_layer_options_container.counts[string.split(" ")[0]] -1
    
    for x in range(1, go_to+1):
        active_index +=1
        if x == skip_index:
            active_index += 1 
        layer_orders[x] = tmp_layer_orders2[active_index]
        layer_images[x-1] = tmp_layer_images2[active_index-1]
        
    parent.layer_orders = layer_orders
    parent.composites = layer_images
    parent.total_layers = len(parent.layer_orders)
    parent.layers_box.clear()

    for g in layer_orders:
        parent.layers_box.addItem(layer_orders[g])
    parent.layers_box.setCurrentRow(parent.total_layers-1)
    parent.render()
