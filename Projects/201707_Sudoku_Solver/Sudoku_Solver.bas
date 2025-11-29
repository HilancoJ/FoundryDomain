Attribute VB_Name = "Sudoku_Solver"

'Get the values from the excel sheet into an array
Sub getoriginal()

Dim original(1 To 9, 1 To 9) As Integer     'Store the original values
Dim cand(1 To 9, 1 To 9, 1 To 10) As Integer    'Array containing all the potential candidates for a certain cell
Dim sing(1 To 2) As Integer     'Store the location of the first cell that has only one candidate
Dim empt(1 To 2) As Integer     'Store the location of the first cell that has no candidates. i.e impossible value has occured before, needs to backtrack
Dim fast(1 To 2) As Integer     'Store the location of the first cell that gets iterated
Dim start, finish, total As Single   'Get the timer going
Dim j As Integer

'Time the solver
start = Now

    'Making the entered values equal to the soduko solving matrix
    For h = 1 To 9
        For c = 1 To 9
            Cells(h + 2, c + 16) = Cells(h + 2, c + 1)
        Next c
    Next h

    'Getting the values from the matrix into own array, will use it to solve the sudoku
    For h = 1 To 9
        For c = 1 To 9
            If Cells(h + 2, c + 16) = "" Then
                original(h, c) = 0
            Else
                original(h, c) = Cells(h + 2, c + 16)
            End If
        Next c
    Next h
        
    'Call the candidate function. It will populate each empty cell with all possible candidates
    getcandidates original, cand, sing, empt

    'If there is a single candidate and no empty candidates start filling in the matrix
    Do While sing(1) <> 0 And sing(2) <> 0 And empt(1) = 0 And empt(2) = 0
        original(sing(1), sing(2)) = cand(sing(1), sing(2), 1)
        Cells(sing(1) + 2, sing(2) + 16) = original(sing(1), sing(2))
        getcandidates original, cand, sing, empt
    Loop
    
    'Find the location of the first block to iterate
        j = 0
        For h = 1 To 9
            For c = 1 To 9
                If original(h, c) = 0 Then
                    fast(1) = h
                    fast(2) = c
                    j = 1
                    Exit For
                End If
            Next c
            If j = 1 Then
                Exit For
            End If
        Next h

    'Call the sudoku solving algorithm
    sudokuvirOupa original, cand, sing, empt
    
finish = Now
total = (finish - start) * 24 * 60 * 60
    
    If total > 3600 Then
        total = total / 3600
        MsgBox "The solver finished in " & Round(total, 2) & " hours"
    End If
    
    If total > 60 Then
        total = total / 60
        MsgBox "The solver finished in " & Round(total, 2) & " minutes"
    End If
    
    MsgBox "The solver finished in " & Round(total, 2) & " seconds"


End Sub

Sub sudokuvirOupa(ByRef original() As Integer, ByRef cand() As Integer, ByRef sing() As Integer, ByRef empt() As Integer)

Dim loca(1 To 2) As Integer     'Store the location of the first empty cell. i.e can be populated with a candidate
Dim temp(1 To 9, 1 To 9) As Integer     'Array used to store the current puzzle. Used to ensure original matrix can be revisited when backtracking
Dim candloop() As Integer       'Array used to iterate through potential candidates for a single cell
Dim w, j, t, g As Integer       'Where the magic happens

'Call the candidate function. It will populate each empty cell with all possible candidates
getcandidates original, cand, sing, empt

    'If there is a single candidate and no empty candidates start filling in the matrix
    Do While sing(1) <> 0 And sing(2) <> 0 And empt(1) = 0 And empt(2) = 0
        original(sing(1), sing(2)) = cand(sing(1), sing(2), 1)
        Cells(sing(1) + 2, sing(2) + 16) = original(sing(1), sing(2))
        getcandidates original, cand, sing, empt
    Loop

    'If there are no candidates for a cell, exit the sub into level before. i.e backtrack
    If empt(1) <> 0 Or empt(2) <> 0 Then
        'MsgBox "Checker"
        Exit Sub
    End If
    
    'Check if the original array has any unfilled blocks
    w = 0
    For h = 1 To 9
        For c = 1 To 9
            If original(h, c) = 0 Then
                w = w + 1
            End If
        Next c
    Next h

    'If there are unfilled blocks, start the iteration and backtracking
    If w <> 0 Then
 
        'Before editing the original array, keep a copy of it to attempt iterations with new values
        For h = 1 To 9
            For c = 1 To 9
                temp(h, c) = original(h, c)
            Next c
        Next h
    
        'Find the location of the first block to iterate
        j = 0
        For h = 1 To 9
            For c = 1 To 9
                If original(h, c) = 0 Then
                    loca(1) = h
                    loca(2) = c
                    j = 1
                    Exit For
                End If
            Next c
            If j = 1 Then
                Exit For
            End If
        Next h
    
        'Find the number of candidates for the first location to iterate
        t = 1
        Do While cand(loca(1), loca(2), t) <> 0
            t = t + 1
        Loop
        t = t - 1
    
        ReDim candloop(1 To t)
        
        'Copy the candidates into the temporary single dimension array
        For h = 1 To t
            candloop(h) = cand(loca(1), loca(2), h)
        Next h
    
        'Go through each candidate for a specific cell
        For Each h In candloop
            'Clear the array of all iterations attempted before doing the new candidate
            For c = 1 To 9
                For j = 1 To 9
                    original(c, j) = temp(c, j)
                    If original(c, j) = 0 Then
                        Cells(c + 2, j + 16) = ""
                    Else
                        Cells(c + 2, j + 16) = original(c, j)
                    End If
                Next j
            Next c
            
            'Put the first candidate into the first empty location
            original(loca(1), loca(2)) = h
            Cells(loca(1) + 2, loca(2) + 16) = original(loca(1), loca(2))
            
            'Call the function again to step into the deep end
            sudokuvirOupa original, cand, sing, empt
                       
            'If all the cells contain a value, exit the function
            g = 0
            For c = 1 To 9
                For j = 1 To 9
                    If original(c, j) = 0 Then
                        g = g + 1
                    End If
                Next j
            Next c
       
            If g = 0 Then
                Exit Sub
            End If
    
        Next h

    End If

End Sub


Sub getcandidates(ByRef original() As Integer, ByRef cand() As Integer, ByRef sing() As Integer, ByRef empt() As Integer)

Dim possib(1 To 9) As Integer   'Array to store all possible candidates
Dim k, t As Integer     'Where the magic happens

'Ensure a fresh candidate array is created
Erase cand

    'Loop through rows and columns
    For h = 1 To 9
        For c = 1 To 9
            '"k" is used to ensure the candidate is entered into the "cand" array in sequential manner
            k = 1
            'If the cell is originally empty, find its candidates
            If original(h, c) = 0 Then
                'Start by giving each cell all candidates and if the candidate is found in the specific row, col or block remove it
                For w = 1 To 9
                    possib(w) = w
                Next w
                
                For w = 1 To 9
                    For j = 1 To 9
                        'Loop through rows
                        If possib(w) = original(h, j) Then
                            possib(w) = 0
                        End If
                        'Loop through columns
                        If possib(w) = original(j, c) Then
                            possib(w) = 0
                        End If
                    Next j
                        
                    'Loop through blocks. Due to excels rounding function, had to implement different cases for certain blocks. Namely when rounding a negative number. It rounds down towards negative infinity, not zero.
                    If h < 4 And c < 4 Then
                    
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                    
                    End If
                    If h < 4 And c > 3 Then
                            
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundDown((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                    
                    End If
                    If h > 3 And c < 4 Then
                        
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundDown((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                        
                    End If
                    If h > 3 And c > 3 Then
                                         
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 1, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 2, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 1) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 2) Then
                                possib(w) = 0
                            End If
                            If possib(w) = original(3 * Application.WorksheetFunction.RoundUp((h / 3 - 1), 0) + 3, 3 * Application.WorksheetFunction.RoundUp((c / 3 - 1), 0) + 3) Then
                                possib(w) = 0
                            End If
                            
                    End If
                    
                    'Will add the candidate if all conditions are satisfied
                    If possib(w) <> 0 Then
                        cand(h, c, k) = w
                        k = k + 1
                    End If
                Next w
            'If the original array has a value in it, give it to make it the only candidate
            Else
                cand(h, c, 1) = original(h, c)
            End If
        Next c
    Next h
    
    'Clear the array that stores the empty and singular candidates
    Erase empt
    Erase sing
    
    'Find the first empty candidate
    t = 0
    For h = 1 To 9
        For c = 1 To 9
                If cand(h, c, 1) = 0 Then
                    empt(1) = h
                    empt(2) = c
                    t = 1
                    Exit For
                End If
        Next c
        If t = 1 Then
            Exit For
        End If
    Next h
    
    'Find the first single candidate
    t = 0
    For h = 1 To 9
        For c = 1 To 9
            '"k" is used to check if there is only one candidate
            k = 0
            For w = 1 To 9
                If cand(h, c, w) <> 0 And original(h, c) = 0 Then
                    k = k + 1
                End If
            Next w
            
            If k = 1 Then
                sing(1) = h
                sing(2) = c
                t = 1
                
                'MsgBox "Go Next"
                
                Exit For
            End If
            
        Next c
        If t = 1 Then
            Exit For
        End If
    Next h

End Sub

Sub Clearall()
    
   For h = 1 To 9
       For c = 1 To 9
            Cells(h + 2, c + 1) = ""
           Cells(h + 2, c + 16) = ""
       Next c
   Next h

End Sub