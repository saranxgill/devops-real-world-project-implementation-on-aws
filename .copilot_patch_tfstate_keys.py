from pathlib import Path
import re
root = Path('.')
pattern = re.compile(r'^(?P<indent>\s*key\s*=\s*")(?P<path>(vpc|eks|retail-persistent-endpoints|karpenter|metrics-server)/dev/terraform\.tfstate)(".*)$')
changed = []
for tf in root.rglob('*.tf'):
    text = tf.read_text(encoding='utf-8')
    new_text = []
    modified = False
    prefix = tf.parts[0]
    for line in text.splitlines(True):
        m = pattern.match(line)
        if m:
            current_path = m.group('path')
            if not current_path.startswith(prefix + '/'):
                new_path = f"{prefix}/{current_path}"
                new_text.append(f"{m.group('indent')}{new_path}{m.group(4)}\n")
                modified = True
                continue
        new_text.append(line)
    if modified:
        tf.write_text(''.join(new_text), encoding='utf-8')
        changed.append(str(tf))
print('PATCHED', len(changed))
for path in changed:
    print(path)
