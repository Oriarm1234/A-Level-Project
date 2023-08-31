import threading
import time

class Event:
  def __init__(self,name):
    self._flag = False
    self.name = name

  def set(self, percentage):
    self._flag = percentage == 100
    self._percentage = percentage

  def is_set(self):
    return self._flag

  def percentage(self):
    return self._percentage

def load_files(event):
  # Load game files in the background
  percentage = 0
  a = [1,2,3,4,5,6,7,8,9,10]
  for file in a:
    percentage += 10
    event.set(percentage)
    time.sleep(0.4)
    # Do something with the file

def generate_terrain(event):
  # Generate terrain in the background
  percentage = 0
  
  a = [1,2,3,4,5,6,7,8,9,10]
  for point in a:
    percentage += 10
    event.set(percentage)
    time.sleep(0.2)
    # Do something with the point

def play_animation(*events):
  # Play animation on the screen
  # Wait for the two threads to finish
  is_set = all(list(event.is_set() for event in events))
  while not is_set:
    is_set = all(list(event.is_set() for event in events))
    message = ", ".join(f"{event.name}: {event.percentage()}%" for event in events)
    print(message)


if __name__ == "__main__":
  # Create two threads

  load_files_event = Event("load_files")
  generate_terrain_event = Event("gen_terrain")

  load_files_thread = threading.Thread(target=load_files,args=[load_files_event])
  generate_terrain_thread = threading.Thread(target=generate_terrain,args=[generate_terrain_event])

  # Start the threads
  load_files_thread.start()
  generate_terrain_thread.start()

  # Play the animation
  play_animation(load_files_event,generate_terrain_event)
