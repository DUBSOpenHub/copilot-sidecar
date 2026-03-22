## 📝 What does this PR do?

_Describe your changes in plain English. One or two sentences is fine._

## 🔗 Related issue

Closes #<!-- issue number -->

## 🧪 Testing checklist

_Please verify all of these before requesting review:_

- [ ] `bash -n sidecar.sh` passes (no shell syntax errors)
- [ ] `bash -n install.sh` passes (no shell syntax errors)
- [ ] All JSON files are valid (`python3 -c "import json, glob; [json.load(open(f)) for f in glob.glob('sidecar/*.json')]"`)
- [ ] `python3 -m pytest test_open.py test_sealed.py -q` — all tests pass
- [ ] Ran a full flow test: `sidecar` launches and shows narration
- [ ] Checked `sidecar --solo` works (if you changed the launcher)

## 📸 Screenshots

_If this changes anything visible, paste before/after screenshots._

## 🗒️ Notes for reviewers

_Anything reviewers should know? Tricky parts? Things you're unsure about?_

---

> 💡 **Tip:** If you're not sure about something, that's OK! Open the PR anyway
> and mention what you'd like help with. We're friendly here. 🤝
