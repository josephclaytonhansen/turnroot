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
            parent.layers_box.setCurrentRow(len(tmp_layer_orders))

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
