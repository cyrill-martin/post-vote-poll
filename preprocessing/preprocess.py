import os
import json
from pathlib import Path
from openpyxl import load_workbook

def create_poll_messages(poll=None) -> dict:
  return {
    "no_poll_id": "You have to indicate a poll ID",
    "no_poll_folder": f"There's no 'polls' folder with a poll subfolder matching the indicated poll ID {poll}",
    "no_codebook": f"There's no codebook matching the indicated poll ID {poll}",
    "no_data": f"There's no data matching the indicated ID {poll}"
  }

def create_poll_paths(poll=None) -> dict: 
  return {
    "poll": f"polls/{poll}",
    "codebook": f"polls/{poll}/{poll}.00-codebuch-zur-nachbefragung.xlsx",
    "data": f"polls/{poll}/{poll}.00-datensatz-der-nachbefragung.csv"
  }

def precheck(poll=None) -> bool:
  """
    Function to precheck if poll data is available or not.
  """

  messages = create_poll_messages(poll)
  paths = create_poll_paths(poll)

  if poll is None:
    print(messages["no_poll_id"])
    return False
  else: 
    # Check if poll subfolder exists
    if not os.path.isdir(paths["poll"]):
      print(messages["no_poll_folder"])
      return False
    else: 
      # Create file paths
      codebook = Path(paths["codebook"])
      data = Path(paths["data"])
      # Check if poll files exist
      if not codebook.exists():
        print(messages["no_codebook"])
        return False
      elif not data.exists(): 
        print(messages["no_data"])
        return False
      else: 
        # Everyting there
        return True

def save_results(poll, name, data) -> None:
  with open(f"polls/{poll}/{poll}_{name}.json", "w", encoding="utf-8") as file:
    json.dump(
      data,
      file, 
      ensure_ascii=False, 
      indent=4
    )

def clean_cell(cell) -> str: 
  string = str(cell)
  str_list = string.split("  ")
  str_list = filter(lambda i: i != "", str_list)
  string = " ".join(str_list)
  string = string.strip()
  string = string.replace("  ", " ")
  return string

def preprocess(poll) -> None:
  """
    Function to preprocess post-vote poll data. 
    The functions reads the codebook of a specific post-vote poll
    and generates corresponding arrangements.json and selections.json files. 
    The function requests a swissvote vote number parameter to find
    post-vote poll data in a corresponding subfolder.
    :param poll: int
  """

  wb = load_workbook(filename = f"polls/{poll}/{poll}.00-codebuch-zur-nachbefragung.xlsx")
  codebook = wb["Codebook"]

  min_row = codebook.min_row
  max_row = codebook.max_row

  min_col = 1
  max_col = 5

  de_col = 3
  fr_col = 4
  it_col = 5

  lang_columns = {
    de_col: "de",
    fr_col: "fr",
    it_col: "it"
  }

  selections = {}
  arrangements = {}

  curr_super_sel = "_-_"
  curr_sel = ""
  curr_att = ""
  is_super_selection = False
  is_selection = False

  skip_indicators = [1939, "[JJJJ]", "[offene Nennung]"]
  continous_indicators = ["birthyearr"]
  delete_indicators = ["control1", "control3", "control3@"]

  def create_selection(cell) -> None: 
    if curr_sel.startswith(curr_super_sel):
      selections[curr_super_sel]["selections"][curr_sel][lang_columns[cell.column]] = clean_cell(cell.value)
    else: 
      selections[curr_sel][lang_columns[cell.column]] = clean_cell(cell.value)

  def create_arrangement(cell) -> None:
    arrangements[curr_sel][curr_att][lang_columns[cell.column]] = clean_cell(cell.value)

  # Iterate rows in codebook (starting from 2nd row)
  for row in codebook.iter_rows(
    min_row=min_row + 1, 
    max_row=max_row, 
    min_col=min_col, 
    max_col=max_col
  ):

    if row[1].value in skip_indicators: 
      # Skip row
      continue

    if str(row[2].value).strip() in skip_indicators:
      # Try to remove already added keys from dicts
      selections.pop(curr_sel, False)
      arrangements.pop(curr_sel, False)
      # Skip row
      continue

    # Iterate cells in codebook row
    for cell in row:

      if cell.column == 1 and cell.value != None:
        # Set super selection
        curr_super_sel = cell.value
        # Already add super selection to dict
        selections[curr_super_sel] = {
          "de": row[de_col - 1].value,
          "fr": row[fr_col - 1].value,
          "it": row[it_col - 1].value,
          "selections": {}}
      elif cell.column == 1 and cell.value == None:
        # Skip cell
        continue

      elif cell.column == 2:
        # It's a code!

        if str(cell.value).isnumeric() == False and cell.value != None:
          # It's a selection
          is_super_selection = False
          is_selection = True
          # Set current selection
          curr_sel = cell.value

          # Create keys in final objects
          if curr_sel.startswith(curr_super_sel):
            selections[curr_super_sel]["selections"][curr_sel] = {}
          else:
            selections[curr_sel] = {}

          if curr_sel not in continous_indicators:
            arrangements[curr_sel] = {}

        elif str(cell.value).isnumeric() == True and cell.value != None:
          # It's a selection attribute
          is_super_selection = False
          is_selection = False
          # Set current attribute
          curr_att = cell.value
          # Create subkey in final arrangements object
          arrangements[curr_sel][cell.value] = {}

        else:
          # It's a super selection!
          # See if cell.column == 1 and cell.value != None
          is_super_selection = True
          # Skip cell
          continue

      else: 
        # It's a label!
        if not is_super_selection:
          if is_selection:
            # It's a selection key
            create_selection(cell)
          else:
            # It's a selection attribute
            create_arrangement(cell)

  # Remove controls
  for item in delete_indicators:
    selections.pop(item, False)
    arrangements.pop(item, False)

  # Save results
  save_results(poll, "selections", selections)
  save_results(poll, "arrangements", arrangements)
 
if __name__ == "__main__":
  print("Poll ID?")
  poll = input()
  if precheck(poll):
    preprocess(poll)