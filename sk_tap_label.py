from math import *
import pyto_ui as ui
from rubicon.objc import *
from Foundation import NSBundle
from mainthread import mainthread

NSBundle.bundleWithPath_('/System/Library/Frameworks/SpriteKit.framework').load()

UIApplication = ObjCClass('UIApplication')
SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKLabelNode = ObjCClass('SKLabelNode')
#SKPhysicsBody = ObjCClass('SKPhysicsBody')
UIColor = ObjCClass('UIColor')

def get_screen_size():				
  app = UIApplication.sharedApplication.keyWindow
  for window in UIApplication.sharedApplication.windows:
    ws = window.bounds.size.width
    hs = window.bounds.size.height
    break
  return ws,hs
    
# We subclass SKScene
class MyScene(SKScene):
    
  # Overriding update_
  @objc_method
  def update_(self, current_time):
    pass
    
   # Overriding touchesBegan_withEvent_
  @objc_method
  def touchesBegan_withEvent_(self, touches, event):
    scene = self
    touch = touches.anyObject()

    point = touch.locationInNode_(scene)
    scene.node.position = point
    if point.x > self.scene.size.width/2:
      scene.backgroundColor = UIColor.redColor
    else:
      scene.backgroundColor = UIColor.blueColor


class DemoView(ui.View):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    b_start = ui.ButtonItem()
    b_start.title = 'start'
    b_start.action = self.b_start_action
    self.b_start = b_start
    self.button_items = [b_start] 
    
  @mainthread
  def did_appear(self):
    #SKView can only be created on a presented view
    #Setup SKView
    screen_size = get_screen_size()
    sz = CGSize(screen_size[0], screen_size[1]-100)
    self.sz = sz
    rect = CGRect(CGPoint(0, 0), sz)
    self.rect = rect
    skview = SKView.alloc().initWithFrame_(rect)
    skview.preferredFramesPerSecond = 30
    self.__py_view__.managed.addSubview(skview)
    self.skview = skview
    
  def b_start_action(self, sender):
    view.title = 'Running'
    self.b_start.title = 'restart'
    
    scene = MyScene.sceneWithSize_(self.rect.size)
    scene.backgroundColor = UIColor.blackColor
    self.skview.presentScene_(scene)
    self.scene = scene
    
    node = SKLabelNode.alloc().init()
    node.text = 'Pyto is good for you'
    node.fontColor = UIColor.whiteColor
    node.fontName = 'Helvetica'
    node.fontSize = 20
    node.position = CGPoint(self.sz.width/2, self.sz.height/2)
    self.scene.addChild_(node)
    self.scene.node = node
    
  
  def did_disappear(self):
    self.skview.paused = True

if __name__ == '__main__':
  view = DemoView()
  view.title = 'SK Pendule'
  ui.show_view(view,ui.PRESENTATION_MODE_FULLSCREEN)
  
  
  
  
  
  
  #end