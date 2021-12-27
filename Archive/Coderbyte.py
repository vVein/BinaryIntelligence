def TreeConstructor(strArr):

  strArr = [ [int(digit) for digit in pair.replace('(','').replace(')','').split(',') ] for pair in strArr ]

  top_index = 0
  top_pair = strArr[top_index]
  complete_pass_through = 0
  max_index = len(strArr)
  failsafe_limit = pow(max_index, 2)
  failsafe = 0

  while complete_pass_through < 1 and failsafe < failsafe_limit:
    failsafe = failsafe + 1
    for index, pairs in enumerate(strArr):
      if pairs[0] == top_pair[1]:
        top_pair = pairs
        top_index = index
        break
      if index + 1 == max_index:
        complete_pass_through = 1

  tree = []
  row = 0
  new_row = 1
  pop = strArr.pop(top_index)
  tree.append([row, pop])

  complete_pass_through = 0
  second_break = False
  failsafe = 0
  sub_tree = [new_row]
  while complete_pass_through < 2 and failsafe < failsafe_limit:
    failsafe = failsafe + 1
    max_index = len(strArr)
    if max_index == 0:
      complete_pass_through = 2
      break

    for arr_index, pairs in enumerate(strArr):

      if second_break:
        second_break = False
        break
      tree_row = len(tree[row])
      for tree_index in range(1, tree_row):


        if row == 0 and pairs[1] == tree[row][tree_index][1]:

          pop = strArr.pop(arr_index)
          tree[row].append(pop)
          complete_pass_through = 0
          second_break = True
          break

        if pairs[1] == tree[row][tree_index][0]:

          pop = strArr.pop(arr_index)
          sub_tree.append(pop)
          complete_pass_through = 0
          second_break = True
          break

      if arr_index + 1 == max_index:
        tree.append(sub_tree)
        row = row + 1
        new_row = new_row + 1
        complete_pass_through = complete_pass_through + 1
        second_break = True
        sub_tree = [new_row]
        break
  

  remaining_pairs = len(strArr)
  if remaining_pairs > 0:
    strArr = 'false'
    return strArr

  unique_check = []
  tally_list = []
  for rows in tree:
    for index, pairs in enumerate(rows):
      if index != 0:
        unique_check.append(pairs[0])
        tally_list.append(pairs[1])
  
  unique_set = set(unique_check)
  if len(unique_set) != len(unique_check):

    strArr = 'false'
    return strArr

  tally_count = [[var, tally_list.count(var)] for var in set(tally_list)]

  tallies = [tally for val, tally in tally_count]
  if max(tallies) > 2:
    strArr = 'false'
    return strArr

  strArr = 'true'
  return strArr


# keep this function call here 
print(TreeConstructor(["(2,3)", "(1,2)", "(4,9)", "(9,3)", "(12,9)", "(6,4)"]))