import streamlit as st
from PIL import Image
import os.path

path_to_image= os.path.join(os.path.dirname(__file__), './images', 'fig1.jpg')


menu = st.sidebar.radio('***',
    (
    'Модель','Дискретизация','ALE'
     )
)
if menu == 'Модель':
    
    st.write('''
    ### Математическая постановка
            ''')

    st.markdown(r'''
    Рассмотрим систему из m законов сохранения в фиксированной области $\Omega \in \mathbb{R}^d$ и подчиняющихся граничным условиям

    $$\dfrac{\partial U}{\partial t} + \nabla F(U) = 0, \qquad in \ \Omega \times [0,T] $$

    где:
    * $U : \Omega \times [0,T] \rightarrow \mathbb{R}^m$ - решение системы
    * $F : \mathbb{R}^m \rightarrow \mathbb{R}^{m\times d}$ - функция потока
    * $\nabla := (\partial_{x_1},\dots,\partial _{x_d})$ - градиент в физической области, такой, что $\nabla W(x,t) = [\partial_{x_1}W(x,t) \dots \partial_{x_d}W(x,t)] \in \mathbb{R}^{N\times d}$ для любого $W : \Omega \times [0,T] \rightarrow \mathbb{R}^N$ и $x \in \Omega, t \in [0,T]$ и граница области $\partial \Omega$ имеет единичную нормаль $n : \partial \Omega \rightarrow \mathbb{R}^d$.

    Закон сохранения дополняется начальным условием $U(x,0) = \overline{U}(x) $ для всех $x \in \Omega$ где $\overline{U} : \Omega \rightarrow \mathbb{R}^m$

    В общем случае решение может содержать разрывы и в этом случае закон сохранения выполняется вдали от разрывов, а условия Рэнкина-Гюгонио выполняются при разрывах.

    В этой работе рассматривается метод высокго порядка, который отслеживается разрывы в вычислительной сетке по мере их развития, что предъявляется требования к дискретизации:
    * дискретизация высокого порядка, стабильная и сходящаяся к закону сохранения 
    * используется базис (базисные функции), которые поддерживают разрывы между ячейками или элементами
    * разрешает деформацию расчетной области

    Таким образом, метод основан на стандратной дискретизации DG-DIRK высокого порядка произвольной лагранжево-эйлеровой формулировке


    ''')

if menu == 'Дискретизация':

    st.markdown(r'''
    ### Дискретизация закона сохранения

    с использование DG таким образом, что закон сохранения сводится к полудискретной форме $\bold{r(\dot u, u, \dot x, x) = 0}$ где $\bold{r}: \mathbb{R}^{N_u} \times \mathbb{R}^{N_u} \times \mathbb{R}^{N_x} \times \mathbb{R}^{N_x} \rightarrow \mathbb{R}^{N_u}$ где $\bold{u} $ - полудискретное представление $U$ из закона сохранения, а $\bold{x}$ - полудискретное представление области $\Omega$ (узловые координаты укзлов сетки)

    Затем применяется временная дискретизация высокого порядка с помощью диагонально неявного метода Рунге-Кутты, чтобы получить полную дискретизацию.


    ''')

if menu == 'ALE':

    st.markdown(r'''
    ### Лагранжево-эйлерова формулировка

    Используется формулировка произвольных лагранжево-эйлерова определяющих уравнений для учета деформаций, зависящих от времени, необходимых для отcлеживания неоднородностей по мере их развития.
    С этой целью вводится зависящее от времени отображение области
    
    $\Im : \Omega_0 \times [0.T] \to \Omega; \hspace{3cm} \Im: (X,t) \mapsto \Im(X,t)$
    
    где $\Omega \subset \mathbb{R}^d $ - фиксированная область
    
    $\quad T$ - финальное время и в каждый момент времени $t \in [0,T], \Im(\cdot,t) : \Omega_0 \to \Omega$ - деффеоморфизм (diffeomorphism).
    ''')
    st.image(Image.open(path_to_image),use_column_width = True,)

    st.markdown(r'''
    В соотвествии с отображением домена, закон сохранения становится

    $$\dfrac{\partial U}{\partial t} + \nabla F(U) = 0, \qquad in\ \Im(\Omega_0,t)$$

    Закон сохранения в физической области $\Omega$ преобразуется в закон сохранения в ис области (reference domain) $\Omega_0$

    $$\dfrac{\partial U_X}{\partial t} + \nabla_X F_X(U_X,G,v) = 0, \qquad in \quad \Omega_0$$

    где $U_X: \Omega \times [0,T] \to \mathbb{R}^m $ - решение преобразованного закона сохранения, 
    
    $F_X: \mathbb{R}^m \times \mathbb{R}^{d \times d} \times \mathbb{R}^d \to \mathbb{R}^{m\times d}$ - преобразованная функция потока

    $\nabla_X := (\partial_{X_1}, \dots, \partial_{X_d})$ - оператор градиента в опорной области

    $G: \Omega_0 \times [0,T] \to \mathbb{R}^{d \times d}$ - градиент деформаций

    Детерминант матрицы Якоби $g : \Omega_0 \times [0,T] \to \mathbb{R}$ и скорости $v: \Omega_0 \times [0,T] \to \mathbb{R}^d$ определяются как: $G = \nabla_X\Im \hspace{2cm} g = det G \hspace{2cm} v = \dfrac{\partial\Im}{\partial t}$ 

    Преобразованное и физическое решения связаны для любых $X \in \Omega_0$ и $t \in [0,T] $ как 

    $U_X (X,t) = g(X,t)U(\Im(X,t),t)$

    И преобразованный поток определяется как:

    $F_X: (W_x,\Theta,\xi) \mapsto [(det\Theta)F((det\Theta)^{-1}W_X)- W_X \otimes \xi]\Theta^{-1}$

    Единичные нормали в эталонной (reference) и физической областях связаны формулой

    $n = \dfrac{gG^{-1}N}{||gG^{-1}N||}$

    Преобразованный закон сохранения дополняется начальным условием 
    $U_X(X,0) = \overline{U}_X(X)$ для всех $X \in \Omega_)$, где $\overline{U}_X : \Omega_0 \to \mathbb{R}^m ;\quad \overline{U}_X = g(X,0)\overline{U}(\Im(X,0))$

    В этой работе эталонная область принимается за физическую область в момент времени 0, что подразумевает $g(X,0) = 1$
    ''')


