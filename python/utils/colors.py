import os
class tcolors:
   W  = '\033[0m'  # white (normal)
   R  = W # red
   G  = W # green
   O  = W # orange
   B  = W # blue
   C  = W # cyan
   Y  = W # yellow
   BOLD = W
   UNDERLINE = W
   use_colors  = os.getenv('USE_COLORS')
   if use_colors:
      R  = '\033[91m' # red
      G  = '\033[92m' # green
      O  = '\033[33m' # orange
      B  = '\033[94m' # blue
      C  = '\033[96m' # cyan
      Y  = '\033[93m' # yellow
      BOLD = '\033[1m'
      UNDERLINE = '\033[4m'
