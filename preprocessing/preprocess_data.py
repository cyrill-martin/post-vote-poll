def poll_vote_info() -> dict:
  return {
    645: {
      "vote": 5, # In the codebook, vote 645 is discussed as vote5, etc.
      "nr_of_votes": 5 # In the codebook, a total of 5 votes is discussed
    },
    644: {
      "vote": 4,
      "nr_of_votes": 5
    },
    643: {
      "vote": 3,
      "nr_of_votes": 5
    },
    642: {
      "vote": 2,
      "nr_of_votes": 5
    },
    641: {
      "vote": 1,
      "nr_of_votes": 5
    },
  }

def column_info() -> dict:
  dic = {
    "min_col": 1,
    "max_col": 5,
    "de_col": 3,
    "fr_col": 4,
    "it_col": 5
  }

  dic["lang_columns"] = {
    dic["de_col"]: "de",
    dic["fr_col"]: "fr",
    dic["it_col"]: "it"
  }
  return dic

# min_col = 1
# max_col = 5

# de_col = 3
# fr_col = 4
# it_col = 5

# lang_columns = {
#   de_col: "de",
#   fr_col: "fr",
#   it_col: "it"
# }

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
    "codebook_sheet": "Codebook",
    "data": f"polls/{poll}/{poll}.00-datensatz-der-nachbefragung.csv"
  }

def create_target_paths(poll, name) -> dict:
  return {
    "target_dir": f"../public/data/polls/{poll}",
    "target_file": f"../public/data/polls/{poll}/{poll}_{name}.json"
  }

def poll_ids() -> list:
  # poll_ids = [636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647]
  poll_ids = [641, 642]
  return poll_ids

def polls_with_semicolon() -> list:
  return [641, 642, 643, 644, 645]

def skip_indicators() -> list:
  # Skip rows with this in column 2 or 3
 return [1939, "[JJJJ]", "[offene Nennung]"]

def continous_indicators() -> list:
  return ["birthyearr"]

def delete_indicators() -> list:
  return [
    "control1",
    "control3",
    "control3@",
    "GEWVORL1",
    "GEWVORL2",
    "GEWVORL3",
    "GEWVORL4",
    "GEWVORL5",
    "GEWVORL6"
  ]

def abc() -> list:
  return ["a", "b", "c", "d", "e", "f", "g", "h"]

def keys_to_remove_by_nr(vote_nr) -> list:
  """
    The codebook by swissvotes handles multiple votes from a given date.
    This function is used to create all the keys to be removed from
    the selections, arrangements, and data objects that are not dealing with
    the currently handled vote.
    :param vote_nr: int
  """
  return [
    f"vote{vote_nr}",
    f"vote{vote_nr}a",
    f"vote{vote_nr}b",
    f"vote{vote_nr}c",
    f"importance{vote_nr}",
    f"difficul{vote_nr}",
    f"dectime{vote_nr}"
  ]

def keys_to_remove_by_letter(letter) -> list:
  """
    The codebook by swissvotes handles multiple votes from a given date.
    This function is used to create all the covid keys to be removed from
    the selections, arrangements, and data objects that are not dealing with
    the currently handled vote. The vote_nr matches the index in the alphabet.
    :param letter: str
  """
  return [
    f"covid1{letter}"
  ]

def keys_to_remove_by_start(vote_nr) -> list:
  """
    The codebook by swissvotes handles multiple votes from a given date.
    This function is used to create all the starting letters of the keys to be removed from
    the selections, arrangements, and data objects that are not dealing with
    the currently handled vote.
    :param vote_nr: int
  """
  return [
    f"reason1acc{vote_nr}",
    f"reason2acc{vote_nr}",
    f"reason1den{vote_nr}",
    f"reason2den{vote_nr}",
    f"argu{vote_nr}"
  ]
