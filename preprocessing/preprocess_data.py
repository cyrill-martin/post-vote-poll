def poll_ids() -> list:
  poll_ids = [648, 649, 650]
  return poll_ids

def polls_with_semicolon() -> list:
  return [641, 642, 643, 644, 645, 648, 649, 650]

def poll_vote_info() -> dict:
  return {
    650: {
        "vote": 3,
        "nr_of_votes": 3
    },
    649: {
        "vote": 2,
        "nr_of_votes": 3
    },
    648: {
        "vote": 1,
        "nr_of_votes": 3
    },
    647: {
      "vote": 2, 
      "nr_of_votes": 2 
    },
    646: {
      "vote": 1, 
      "nr_of_votes": 2 
    },
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
    640: {
      "vote": 3,
      "nr_of_votes": 3
    },
    639: {
      "vote": 2,
      "nr_of_votes": 3
    },
    638: {
      "vote": 1,
      "nr_of_votes": 3
    },
    637: {
      "vote": 2,
      "nr_of_votes": 2
    },
    636: {
      "vote": 1,
      "nr_of_votes": 2
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
    "target_dir": f"../public/data/{poll}",
    "target_file": f"../public/data/{poll}/{poll}_{name}.json"
  }

def skip_indicators() -> list:
  # Skip rows with this in column 2 or 3
 return [1939, "[JJJJ]", "[offene Nennung]"]

def continous_indicators() -> list:
  return ["birthyearr".upper()]

def delete_indicators() -> list:
  return [
    "control1".upper(),
    "control3".upper(),
    "control3@".upper(),
    "UNUSED",
    "GEWVORL1",
    "GEWVORL2",
    "GEWVORL3",
    "GEWVORL4",
    "GEWVORL5",
    "GEWVORL6"
  ]

def abc() -> list:
  return ["A", "B", "C", "D", "E", "F", "G", "H"]

def keys_to_remove_by_nr(vote_nr) -> list:
  """
    The codebook by swissvotes handles multiple votes from a given date.
    This function is used to create all the keys to be removed from
    the selections, arrangements, and data objects that are not dealing with
    the currently handled vote.
    :param vote_nr: int
  """
  return [
    f"vote{vote_nr}".upper(),
    f"vote{vote_nr}a".upper(),
    f"vote{vote_nr}b".upper(),
    f"vote{vote_nr}c".upper(),
    f"importance{vote_nr}".upper(),
    f"difficul{vote_nr}".upper(),
    f"dectime{vote_nr}".upper()
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
    f"covid1{letter}".upper()
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
    f"reason1acc{vote_nr}".upper(),
    f"reason2acc{vote_nr}".upper(),
    f"reason1den{vote_nr}".upper(),
    f"reason2den{vote_nr}".upper(),
    f"argu{vote_nr}".upper()
  ]
