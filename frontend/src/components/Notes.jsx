import { useEffect, useState } from 'react';
import { getNotes, addNote } from '../api/api';
import styles from './Notes.module.css';

export default function Notes({ appId }) {
  const [notes, setNotes] = useState([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);

  const load = () => {
    getNotes(appId)
      .then(res => setNotes(res.data))
      .catch(console.error);
  };

  useEffect(() => { load(); }, [appId]);

  const handleAdd = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      await addNote(appId, { note: text });
      setText('');
      load();
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) handleAdd();
  };

  return (
    <div className={styles.wrapper}>
      {notes.length === 0 && (
        <p className={styles.empty}>No notes yet.</p>
      )}
      {notes.map(n => (
        <div key={n.id} className={styles.noteCard}>
          <p className={styles.noteText}>{n.note}</p>
          <span className={styles.noteDate}>
            {new Date(n.created_at).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}
          </span>
        </div>
      ))}
      <textarea
        className={styles.input}
        rows={2}
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={handleKey}
        placeholder="Add a note… (Ctrl+Enter to save)"
      />
      <button className={styles.btn} onClick={handleAdd} disabled={loading}>
        {loading ? 'Saving…' : 'Add Note'}
      </button>
    </div>
  );
}
