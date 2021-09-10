bl_info = {
    "name": "Global Bevel",
    "author": "Shreya Punjabi",
    "version": (1,0),
    "blender": (2, 92, 0),
    "location": "View 3D > Sidebar > Edit > Global Bevel",
    "description": "Global bevels settings for multiple objects",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}



import bpy

global object_list
global object_names
object_list = []
object_names = []

class BEVEL_UI(bpy.types.Panel):
    "Add bevel"
    bl_label = "Global Bevel"
    bl_idname = "BEVEL_ADD_PT_MAIN"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    
    def draw(self, context):
        layout = self.layout
        

        
        
        row = layout.row()
        row.alignment = 'RIGHT'
        row.label(text = "Segments")
        
        row.prop(context.scene, 'segments', text="")
        
        row = layout.row()
        row.alignment = 'RIGHT'
        row.label(text = "Amount")
        row.prop(context.scene, 'width', text="")
        
        row = layout.row()
        row.alignment = 'LEFT'
        #row.label(text = "Smoothing")
        row.prop(context.scene, 'auto_smooth')



        row = layout.row()
        row.operator("bevel.add", icon = "MOD_BEVEL")
    
        
        
        gr = layout.grid_flow(columns=2, even_columns=True)
        #gr=layout.split(factor=0.5)
        
        #viewport visibility toggle
        gr_col = gr.column()
        gr_col.operator("bevel.viewport_vis", text="Viewport", icon="RESTRICT_VIEW_OFF")
        
        #delete all
        gr_col = gr.column()
        gr_col.operator("bevel.delete_all", text="Delete All", icon="TRASH" )
        
        #temp = layout.template_modifiers()
        
        row=layout.row()
        row.separator(factor=0.0)
        
        
        row = layout.row()
        row.alignment = 'LEFT'
        #row.label(text = "Smoothing")
        row.prop(context.scene, 'auto_update')
        
        row = layout.row()
        row.operator("bevel.update_duplicates", icon = "DUPLICATE")
        
        
        
    
class ADD_BEVEL(bpy.types.Operator):
    "Add a global bevel to selected objects"
    bl_idname = "bevel.add"
    bl_label = "Add Bevel" 
    bl_options = {'REGISTER', 'UNDO'} 
    
        

    
    def execute(self, context):
        
        lst = bpy.context.selected_objects
        for i in lst:
            ok=False
            object = bpy.data.objects[i.name]

            for mod in object.modifiers:
                if(mod.name.startswith("Global")):
                    ok=True
            if(ok):
                continue
                
                
            object_list.append(object) 
            object_names.append(object.name)
            
            
            modifier = object.modifiers.new(name="asdf", type='BEVEL')
            modifier.name = "Global_Bevel"
            
            modifier.width = bpy.context.scene.width
            modifier.segments = bpy.context.scene.segments
            
            for polygon in object.data.polygons:
                polygon.use_smooth = True
            
            if (bpy.context.scene.auto_smooth):
                object.data.use_auto_smooth = 1

        return {"FINISHED"}
    
    @classmethod
    def poll(cls, context):
        for i in bpy.context.selected_objects:
            if (i.type != 'MESH'):
                return False
        return True



def get_obj_lst():
    print(object_list)
          




class VIEWPORT_VISBILITY(bpy.types.Operator):
    "Toggle viewport visibility of global bevels"
    bl_idname = "bevel.viewport_vis"
    bl_label = "Viewport Visibility" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        global object_list
        global object_names
        
        if bpy.context.scene.auto_update:
            bpy.ops.bevel.update_duplicates()
        
        loc_copy = object_list.copy()
        loc_names = object_names.copy()
        vis=0

        try:
            for object in loc_copy:

                for mod in object.modifiers:
                    if(mod.name.startswith("Global") and mod.type=="BEVEL"):
                    #if mod.segments==bpy.context.scene.segments and mod.width == bpy.context.scene.width:
                          
                        if (mod.show_viewport):
                            vis+=1
                            #mod.show_viewport = (not mod.show_viewport)
            
            show = False
            show |= (vis>=len(loc_copy)/2)
            
            
            for object in loc_copy:
                for mod in object.modifiers:
                    if(mod.name.startswith("Global") and mod.type=="BEVEL"):
                        #if mod.segments==bpy.context.scene.segments and mod.width == bpy.context.scene.width:
                        mod.show_viewport = not show
        
        except:
            self.report({"WARNING"}, "Please update changes for this to work.")
            return {"CANCELLED"}                  
                    
        return {"FINISHED"}



class DELETE_ALL(bpy.types.Operator):
    "Delete all global bevels"
    bl_idname = "bevel.delete_all"
    bl_label = "Delete All" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        global object_list
        
        loc_copy = object_list.copy()
        
        
        if bpy.context.scene.auto_update:
            bpy.ops.bevel.update_duplicates()
            
        
        try:
        
            for object in loc_copy: 
                
                for mod in object.modifiers:
                    if(mod.name.startswith("Global") and mod.type=="BEVEL"):
                        
                        object.modifiers.remove(mod)
                        object_list.remove(object)
                        #object_names.remove(object.name)
                        
                        #if mod.segments==bpy.context.scene.segments and mod.width == bpy.context.scene.width:
        
        except:
            self.report({"WARNING"}, "Please update changes for this to work.")
            return {"CANCELLED"}                 
                        
                        
               
        return {"FINISHED"}






class UPDATE_DUPLICATES(bpy.types.Operator):
    "Update duplicates, manual deletions, and other changes"
    bl_idname = "bevel.update_duplicates"
    bl_label = "Update Changes" #change
    bl_options = {'REGISTER', 'UNDO'} 
    
    
    

    def execute(self, context):
        global object_list #you have to mention this if you plan to make changes to it
        global object_names
        self.report({"INFO"}, "Updating Global Bevel information. This may take a while depending on the size of the scene.")
        loc_copy = []
        loc_names=[]
        
        for object in bpy.data.objects:
            
            for mod in object.modifiers:
                if(mod.name.startswith("Global") and mod.type=="BEVEL"):
                    loc_copy.append(object)
                    loc_names.append(object.name)
                    
                    mod.segments = bpy.context.scene.segments
                    mod.width = bpy.context.scene.width

        object_list.clear()
        object_names.clear()
        object_list = loc_copy.copy()
        object_names = loc_names.copy()

        return {"FINISHED"}
        
             

def update_segments(self, context):
    loc_copy = object_list.copy()
    
    if bpy.context.scene.auto_update:
        bpy.ops.bevel.update_duplicates()
    
    for object in loc_copy:
            for mod in object.modifiers:
                if(mod.name.startswith("Global") and mod.type=="BEVEL"):
                    #if mod.segments==bpy.context.scene.segments and mod.width == bpy.context.scene.width:
                    mod.segments = bpy.context.scene.segments
                    mod.width = bpy.context.scene.width
                    
                    
                    
                    
def toggle_auto_update(self, context):
    self.report({"WARNING"}, "Leaving this on with large scenes can slow down Blender. Switch to manual updates if you face problems")





def register():
    bpy.utils.register_class(BEVEL_UI)
    bpy.utils.register_class(ADD_BEVEL)
    bpy.utils.register_class(VIEWPORT_VISBILITY)
    bpy.utils.register_class(DELETE_ALL)
    bpy.utils.register_class(UPDATE_DUPLICATES)
    
    bpy.types.Scene.width = bpy.props.FloatProperty \
      (
        name = "Width",
        description = "", #the thing that comes when you hover over it
        default = 0.03,
        min=0.00,
        update = update_segments
      )
      
    bpy.types.Scene.segments = bpy.props.IntProperty \
      (
        
        name = "Segments",
        description = "", 
        default = 3,
        min=1,
        max=100,
        update = update_segments
        
      )
      
      
    bpy.types.Scene.auto_smooth = bpy.props.BoolProperty \
      (
        
        name = "Auto Smooth",
        description = "Set auto smooth of selected objects to True", #the thing that comes when you hover over it
        default = True

      )
      
    bpy.types.Scene.auto_update = bpy.props.BoolProperty \
      (
        
        name = "Auto Update",
        description = "Automatically updates scene information. Disable for heavy scenes.", #the thing that comes when you hover over it
        default = True,

      )
      
      
    

def unregister():
    bpy.utils.unregister_class(BEVEL_UI)
    bpy.utils.unregister_class(ADD_BEVEL)
    bpy.utils.unregister_class(VIEWPORT_VISBILITY)
    bpy.utils.unregister_class(DELETE_ALL)
    bpy.utils.unregister_class(UPDATE_DUPLICATES)

    del bpy.types.Scene.width
    del bpy.types.Scene.segments
    del bpy.types.Scene.auto_smooth
    del bpy.types.Scene.auto_update

    
    
    
if __name__ == "__main__":
    register()
    #unregister()