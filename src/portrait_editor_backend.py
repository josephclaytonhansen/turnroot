def layerDown(parent):
    if parent.layers_box.currentItem() != None:
        for layer in parent.layer_orders:
            if parent.layer_orders[layer] == parent.layers_box.currentItem().text():
                tmp_layer_orders = parent.layer_orders
                check = layer
                
        parent.layer_orders = {}
        try:
            if check < len(tmp_layer_orders):
                for n in tmp_layer_orders:
                    if n == check:
                        parent.layer_orders[check] = tmp_layer_orders[check+1]
                    elif n == check+1:
                        parent.layer_orders[check+1] = tmp_layer_orders[check]
                    else:
                        parent.layer_orders[n] = tmp_layer_orders[n]
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
        except:
            pass

def layerUp(parent):
    if parent.layers_box.currentItem() != None:
        for layer in parent.layer_orders:
            if parent.layer_orders[layer] == parent.layers_box.currentItem().text():
                tmp_layer_orders = parent.layer_orders
                check = layer
                
        parent.layer_orders = {}
        try:
            if check > 1:
                for n in tmp_layer_orders:
                    if n == check:
                        parent.layer_orders[check] = tmp_layer_orders[check-1]
                    elif n == check-1:
                        parent.layer_orders[check-1] = tmp_layer_orders[check]
                    else:
                        parent.layer_orders[n] = tmp_layer_orders[n]
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
        except:
            parent.layers_box.setCurrentRow(0)
            
def layerDelete(parent, layer):
    layer_orders = parent.layer_orders
    tmp_layer_orders = layer_orders
    layer_orders = {}
    tmp_layer_orders2 = tmp_layer_orders.copy()
    tmp_layer_orders2.pop(layer+1)
    go_to = len(tmp_layer_orders2)
    active_index = 0
    skip_index = layer+1
    
    for x in range(1, go_to+1):
        active_index +=1
        if x == skip_index:
            active_index += 1 
        layer_orders[x] = tmp_layer_orders2[active_index]
        
    parent.layer_orders = layer_orders
    parent.total_layers = len(parent.layer_orders)
    parent.layers_box.clear()
    
    for g in layer_orders:
        parent.layers_box.addItem(layer_orders[g])
