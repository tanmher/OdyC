 def program(self):
    res = ParseResult()

    if self.current_tok.matches(TT_KEYWORD, 'TROJAN'):
      res.register_advancement()
      self.advance()

      statements = res.register(self.statements())
      if res.error: return res
      program = (statements, True)
      
      if self.current_tok.matches(TT_KEYWORD, 'HALT'):
        res.register_advancement()
        self.advance()
        
      else:
        return res.failure(InvalidSyntaxError(
          self.current_tok.pos_start, self.current_tok.pos_end,
          "Expected 'HALT'"
        ))
    else:
      statements = res.register(self.statements())
      if res.error: return res
      program = (statements, False)

    if not res.error and self.current_tok.type != TT_EOF:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        "Token cannot appear after previous tokens"
      ))

    return res.success(program)