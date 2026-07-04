import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class AIQASystem:
    """小型人工智能基础问答系统"""
    def __init__(self):
        # 1. 构建知识库
        self.knowledge_base = {
            "什么是人工智能？": "人工智能（AI）是计算机科学的一个分支，旨在创造能够模拟人类智能行为的系统。",
            "Python在人工智能中的作用是什么？": "Python因其简洁的语法和丰富的AI库（如TensorFlow, PyTorch），成为AI开发的首选语言。",
            "机器学习和深度学习有什么区别？": "机器学习是AI的一个子集，而深度学习是机器学习的子集，主要基于人工神经网络处理复杂数据。",
            "什么是自然语言处理（NLP）？": "NLP是AI的分支，致力于让计算机能够理解、解释和生成人类语言。",
            "什么是计算机视觉（CV）？": "CV是AI的一个领域，旨在让计算机能够从图像或视频中获取并理解高层语义信息。",
            "什么是监督学习？": "监督学习是一种机器学习方法，使用带有标签的训练数据来训练模型，使其能够预测未知数据。",
            "什么是无监督学习？": "无监督学习使用没有标签的数据，通过发现数据中的隐藏结构和模式来进行学习。",
            "什么是强化学习？": "强化学习通过智能体与环境交互，根据奖励或惩罚信号来不断调整策略，以最大化累积奖励。",
            "什么是神经网络？": "神经网络是一种受人类大脑启发的计算模型，由大量相互连接的节点（神经元）组成，用于学习复杂的数据表示。",
            "什么是大语言模型（LLM）？": "LLM是基于Transformer架构，在海量文本上预训练的深度学习模型，具备强大的自然语言理解和生成能力。",
            "什么是过拟合？": "过拟合是指模型在训练数据上表现很好，但在未见过的测试数据上表现差，泛化能力弱。",
            "什么是损失函数？": "损失函数用于衡量模型预测值与真实值之间的差异，是模型优化的目标函数。",
            "什么是梯度下降？": "梯度下降是一种优化算法，通过计算损失函数的梯度，迭代更新模型参数以最小化损失。",
            "什么是迁移学习？": "迁移学习是将在一个任务上学到的知识应用到另一个相关任务上，以减少训练时间和数据需求。",
            "什么是Tokenization？": "Tokenization是将文本分割成更小的单元（如词、子词或字符），以便模型能够处理的文本预处理步骤。"
        }
        
        # 2. 提取核心关键词，存入集合（去重）
        self.keywords_set = set()
        self.qa_keywords_map = {} # 记录每个问题对应的关键词集合
        
        for question in self.knowledge_base:
            # 去除标点符号，按字/词拆分作为关键词集合
            clean_q = question.replace("？", "").replace("?", "").replace("（", "").replace("）", "")
            keywords = set(clean_q) 
            self.qa_keywords_map[question] = keywords
            self.keywords_set.update(keywords)

        # 用户提问记录列表
        self.user_history = []

    def get_answer(self, user_question):
        """3. 问答匹配逻辑：利用集合求交集"""
        if not user_question.strip():
            return "请输入有效的问题！"
            
        user_keywords = set(user_question.replace("？", "").replace("?", ""))
        
        max_intersection = 0
        best_match_q = None
        
        # 遍历知识库，计算交集大小
        for q, q_keywords in self.qa_keywords_map.items():
            intersection = len(user_keywords & q_keywords) # 集合求交集
            if intersection > max_intersection:
                max_intersection = intersection
                best_match_q = q
                
        # 记录用户历史
        self.user_history.append(user_question)
        
        if best_match_q and max_intersection > 0:
            return f"【匹配问题】{best_match_q}\n【答案】{self.knowledge_base[best_match_q]}"
        else:
            return "抱歉，未找到相关答案，请尝试其他问题。"

# --- 可视化交互界面 ---
class QASystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI 基础问答系统")
        self.root.geometry("600x500")
        self.qa_system = AIQASystem()

        # 聊天记录显示区
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.insert(tk.END, "🤖 欢迎使用AI基础问答系统！请输入你的问题（输入'退出'结束）。\n\n")

        # 输入区
        input_frame = ttk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.entry = ttk.Entry(input_frame, font=("Microsoft YaHei", 10))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.handle_input) # 支持回车键提问

        ttk.Button(input_frame, text="发送", command=self.handle_input).pack(side=tk.RIGHT)

    def handle_input(self, event=None):
        user_input = self.entry.get().strip()
        if user_input == "退出":
            messagebox.showinfo("系统提示", f"感谢使用！您共提问了 {len(self.qa_system.user_history)} 次。")
            self.root.destroy()
            return
            
        if user_input:
            # 显示用户问题
            self.chat_area.insert(tk.END, f"👤 你: {user_input}\n")
            # 获取系统回答
            answer = self.qa_system.get_answer(user_input)
            self.chat_area.insert(tk.END, f"🤖 AI: {answer}\n\n")
            self.chat_area.see(tk.END) # 自动滚动到最新消息
            self.entry.delete(0, tk.END) # 清空输入框

if __name__ == "__main__":
    root = tk.Tk()
    app = QASystemGUI(root)
    root.mainloop()