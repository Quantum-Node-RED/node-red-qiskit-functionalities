// component.js

class Component {
    constructor(name, parameters = {}) {
        this.name = name;
        this.parameters = parameters;
        this.children = [];
    }

    addChild(child) {
        this.children.push(child);
    }

    toJSON() {
        return {
            name: this.name,
            parameters: this.parameters,
            children: this.children.map(child => child.toJSON())
        };
    }
}    

function addComponentasChild(msg, newNode) {
    if (!msg.payload.structure) {
        // If no structure exists, create a new root
        root=new Component("root", {});
        msg.payload.structure=[];
        msg.payload.structure.push(root);
        msg.payload.structure.push(newNode);
        msg.payload.currentNode = newNode;
        msg.payload.parentofCurrentNode=root;
        msg.payload.no_of_components = msg.payload.no_of_components + 1;
    }
    
    if (msg.payload.currentNode) {
        // Add the new node as a child of the current node
        msg.payload.currentNode.addChild(newNode);
        // Update the current node to the newly added node
        msg.parentofCurrentNode=msg.payload.currentNode;
        // Update the parent of the current node 
        msg.payload.currentNode = newNode;
        // Increment the number of components
        msg.payload.no_of_components = msg.payload.no_of_components + 1;
    } else {
        // If there's no current node, add to the list of structure
        msg.payload.structure.push(newNode);
        // Update the current node to the newly added node
        msg.payload.currentNode = newNode;
        // Update the parent of the current node
        msg.payload.parentofCurrentNode=null;//is this fine?
        // Increment the number of components
        msg.payload.no_of_components = msg.payload.no_of_components + 1;
    }
}

function addComponent(msg,newNode){
    if (!msg.payload.structure) {
        // If no structure exists, create a new root
        root=new Component("root", {});
        msg.payload.structure=[];
        msg.payload.structure.push(root);
        msg.payload.structure.push(newNode);
        msg.payload.currentNode = newNode;
        msg.payload.parentofCurrentNode=root;
        msg.payload.no_of_components = msg.payload.no_of_components + 1;
    }
    
    if (msg.payload.currentNode) {
        //Add to the list of structure
        msg.payload.structure.push(newNode);
        // Update the current node to the newly added node
        msg.parentofCurrentNode=msg.payload.currentNode;
        // Update the parent of the current node 
        msg.payload.currentNode = newNode;
        // Increment the number of components
        msg.payload.no_of_components = msg.payload.no_of_components + 1;
    } else {
        // If there's no current node, add to the list of structure
        msg.payload.structure.push(newNode);
        // Update the current node to the newly added node
        msg.payload.currentNode = newNode;
        // Update the parent of the current node
        msg.payload.parentofCurrentNode=null;//is this fine?
        // Increment the number of components
        msg.payload.no_of_components = msg.payload.no_of_components + 1;
    }
}

function addGateComponentasChild(msg, newNode) {
    if (!msg.payload.structure) {
        // If no structure exists, create a new root
        // If we are to add this newNode to the root can cause a weird structure, like gate component being child of root 
        root = new Component("root", {});
        msg.payload.structure = [root];
        msg.payload.currentNode = root;
        msg.payload.parentofCurrentNode = root;
        msg.payload.no_of_components = 0;
    }
    
    if (msg.payload.currentNode) {
        let targetNode = msg.payload.currentNode;
        // Check if the current node is a gate
        if (msg.payload.currentNode.name.endsWith('-gate')) {
            // If it's a gate, set the target to the parent of the current node
            targetNode = msg.payload.parentofCurrentNode || msg.payload.structure[0]; // Default to root if no parent
        }
        
        // Add the new node as a child of the target node
        targetNode.addChild(newNode);
        
        // Update the current node to the newly added node
        msg.payload.parentofCurrentNode = targetNode;
        msg.payload.currentNode = newNode;
        
        // Increment the number of components
        msg.payload.no_of_components=msg.payload.no_of_components + 1;
    } else {
        // If there's no current node, add to the root of the structure
        msg.payload.structure[0].addChild(newNode);
        msg.payload.currentNode = newNode;
        msg.payload.parentofCurrentNode = msg.payload.structure[0];
        msg.payload.no_of_components=msg.payload.no_of_components++;
    }
}



module.exports = {
    Component,
    addComponentasChild,
    addComponent,
    addGateComponentasChild
};