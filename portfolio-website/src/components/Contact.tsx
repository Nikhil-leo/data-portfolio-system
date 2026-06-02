"use client";
import { useState } from "react";
import { Mail, Github, Linkedin, ExternalLink, Send } from "lucide-react";
import profile from "@/data/profile.json";

export default function Contact() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [sent, setSent] = useState(false);

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    // mailto: fallback — replace with your form backend (Formspree, EmailJS, etc.)
    const subject = encodeURIComponent(`Portfolio Contact from ${form.name}`);
    const body = encodeURIComponent(`Name: ${form.name}\nEmail: ${form.email}\n\n${form.message}`);
    window.open(`mailto:${profile.email}?subject=${subject}&body=${body}`);
    setSent(true);
  }

  return (
    <section id="contact" className="py-24 bg-slate-900/40">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="section-title">
            Get In <span className="gradient-text">Touch</span>
          </h2>
          <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-teal-500 mx-auto rounded mb-4" />
          <p className="text-slate-400 max-w-md mx-auto">
            Have a data project in mind? Let&apos;s talk.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 max-w-4xl mx-auto">
          {/* Contact info */}
          <div>
            <h3 className="text-xl font-semibold mb-6">Contact Info</h3>
            <div className="space-y-4">
              <a href={`mailto:${profile.email}`}
                className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                  <Mail size={18} className="text-blue-400" />
                </div>
                {profile.email}
              </a>
              <a href={profile.github} target="_blank" rel="noreferrer"
                className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                  <Github size={18} className="text-blue-400" />
                </div>
                GitHub
              </a>
              <a href={profile.linkedin} target="_blank" rel="noreferrer"
                className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                  <Linkedin size={18} className="text-blue-400" />
                </div>
                LinkedIn
              </a>
              <a href={profile.tableau} target="_blank" rel="noreferrer"
                className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                  <ExternalLink size={18} className="text-blue-400" />
                </div>
                Tableau Public
              </a>
            </div>
          </div>

          {/* Form */}
          <div>
            <h3 className="text-xl font-semibold mb-6">Send a Message</h3>
            {sent ? (
              <div className="glass-card p-6 text-center">
                <p className="text-teal-400 font-semibold text-lg">Message sent!</p>
                <p className="text-slate-400 text-sm mt-2">
                  Your email client should have opened. I&apos;ll get back to you soon.
                </p>
                <button
                  onClick={() => setSent(false)}
                  className="mt-4 text-sm text-blue-400 hover:text-blue-300"
                >
                  Send another message
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm text-slate-400 mb-1">Name</label>
                  <input
                    name="name" value={form.name} onChange={handleChange}
                    required placeholder="Jane Smith"
                    className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm text-slate-400 mb-1">Email</label>
                  <input
                    name="email" type="email" value={form.email} onChange={handleChange}
                    required placeholder="jane@example.com"
                    className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm text-slate-400 mb-1">Message</label>
                  <textarea
                    name="message" value={form.message} onChange={handleChange}
                    required rows={5} placeholder="Tell me about your project..."
                    className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors resize-none"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full flex items-center justify-center gap-2 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
                >
                  <Send size={16} /> Send Message
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
