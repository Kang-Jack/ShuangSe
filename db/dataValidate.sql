select * from doubleball where (RED1 >RED2 or RED1 >RED3 or RED1 >RED4 or RED1 >RED5 or RED1 >RED6)
 or (RED2>RED3 or RED2>RED4 or RED2>RED5 or RED2>RED6)  or (RED3>RED4 or RED3>RED5 or RED3>RED6)
  or (RED4>RED5 or RED4>RED6) or (RED5>RED6)


select * from doubleball where (RED1 < RED2 and RED2 < RED3 and RED3 < RED4 and RED4 < RED5 and RED5 < RED6) 
 and (BLUE between 1 and 16) and (RED1 between 1 and 33) and (RED2 between 1 and 33) and (RED3 between 1 and 33)
 and (RED4 between 1 and 33) and (RED5 between 1 and 33) and (RED6 between 1 and 33)