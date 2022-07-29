def determinant(m):
    ans,sizeM = 0, len(m)
    if sizeM == 1: return m[0][0]
    for n in range(sizeM):
        ans+= (-1)**n * m[0][n] * determinant([ m[i][:n]+m[i][n+1:] for i in range(1,sizeM) ])
    return ans
