
# def corrButton():
#     corr_data = corrInput.get()
#     correlation(corr_data)
#     corrBtn.flash()


# corrFrame = LabelFrame(root, text="Correlation", padx=20,
#                        pady=20, fg="WHITE", font=("Helvetica", 20, "bold"), labelanchor="n", borderwidth=6, background="BLACK", relief="ridge")
# corrLabel = Label(corrFrame, text="Enter Tikcers", font=(
#     "Helvetica", 16), background="BLACK", fg="WHITE")
# corrInput = Entry(corrFrame,
#                   bg=input_clr,
#                   state="normal",
#                   width=100,
#                   bd=3,
#                   font=("Helvetica", 16),
#                   highlightcolor=high_clr,
#                   highlightthickness=3)
# corrBtn = Button(corrFrame,
#                  text="Check Correlation",
#                  command=corrButton,
#                  font=("Helvetica", 16, "bold"),
#                  background=btn_color,
#                  cursor="exchange",
#                  activebackground=active_btn,
#                  activeforeground=btn_color)
# corrLabel.grid(row=0, column=0, padx=5, pady=5, sticky="W")
# corrInput.grid(row=1, column=0, padx=10, pady=10)
# corrBtn.grid(row=2, column=0, padx=10, pady=10, sticky="E")