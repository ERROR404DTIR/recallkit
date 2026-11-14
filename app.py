#!/usr/bin/env python3
"""RecallKit — local spaced repetition flashcards. Python 3.9+, stdlib only."""
import argparse,csv,datetime as dt,sqlite3,sys
from pathlib import Path
DB=Path(__file__).with_name("recallkit.db")
def connect():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 c.execute("""CREATE TABLE IF NOT EXISTS cards(id INTEGER PRIMARY KEY,front TEXT NOT NULL,back TEXT NOT NULL,due TEXT NOT NULL,interval INTEGER DEFAULT 0,ease REAL DEFAULT 2.5,reps INTEGER DEFAULT 0,created TEXT NOT NULL)"""); return c
def today(): return dt.date.today()
def main():
 p=argparse.ArgumentParser(description="Spaced repetition flashcards"); s=p.add_subparsers(dest="cmd",required=True)
 a=s.add_parser("add"); a.add_argument("front"); a.add_argument("back")
 st=s.add_parser("study"); st.add_argument("-n",type=int,default=20)
 e=s.add_parser("export"); e.add_argument("file")
 im=s.add_parser("import"); im.add_argument("file")
 s.add_parser("stats")
 args=p.parse_args(); c=connect()
 if args.cmd=="add":
  c.execute("INSERT INTO cards(front,back,due,created) VALUES(?,?,?,?)",(args.front,args.back,today().isoformat(),today().isoformat())); c.commit(); print("Card added.")
 elif args.cmd=="study":
  cards=c.execute("SELECT * FROM cards WHERE due<=? ORDER BY due,id LIMIT ?",(today().isoformat(),args.n)).fetchall()
  if not cards: print("Nothing due. You're all caught up."); return
  for x in cards:
   print(f"\n[{x['id']}] {x['front']}"); input("Think of the answer, then press Enter…")
   print("Answer:",x["back"])
   while True:
    try: grade=int(input("Grade 0=Again  1=Hard  2=Good  3=Easy: "))
    except ValueError: grade=-1
    if grade in range(4): break
    print("Enter 0, 1, 2 or 3.")
   reps=x["reps"]+1; ease=max(1.3,x["ease"]+(0.1-(3-grade)*(0.08+(3-grade)*0.02)))
   if grade==0: interval=1; reps=0
   elif reps==1: interval=1
   elif reps==2: interval=3
   else: interval=max(1,round(x["interval"]*ease*(0.65 if grade==1 else 1.0 if grade==2 else 1.25)))
   due=(today()+dt.timedelta(days=interval)).isoformat()
   c.execute("UPDATE cards SET due=?,interval=?,ease=?,reps=? WHERE id=?",(due,interval,ease,reps,x["id"])); c.commit()
   print(f"Next review: {due} ({interval} day(s))")
 elif args.cmd=="stats":
  total=c.execute("SELECT count(*) FROM cards").fetchone()[0]; due=c.execute("SELECT count(*) FROM cards WHERE due<=?",(today().isoformat(),)).fetchone()[0]
  print(f"Total cards: {total}\nDue today: {due}")
 elif args.cmd=="export":
  rows=c.execute("SELECT front,back FROM cards")
  with open(args.file,"w",newline="",encoding="utf-8") as f:
   w=csv.writer(f); w.writerow(["front","back"]); w.writerows(rows)
  print("Exported",args.file)
 elif args.cmd=="import":
  count=0
  with open(args.file,newline="",encoding="utf-8-sig") as f:
   for row in csv.DictReader(f):
    if row.get("front") and row.get("back"):
     c.execute("INSERT INTO cards(front,back,due,created) VALUES(?,?,?,?)",(row["front"],row["back"],today().isoformat(),today().isoformat())); count+=1
  c.commit(); print(f"Imported {count} cards.")
 c.close()
if __name__=="__main__": main()
