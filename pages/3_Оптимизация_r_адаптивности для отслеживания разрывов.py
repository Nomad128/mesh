import streamlit as st
from PIL import Image
import os.path

path_to_image= os.path.join(os.path.dirname(__file__), './images', 'fig1.jpg')

menu = st.sidebar.radio('***',
    (
    'Формулировка ограниченной оптимизации','SQP решатель'
     )
)
if menu =='Формулировка ограниченной оптимизации':

    st.markdown(r'''
    В этом разделе расширяется система отслеживания ударных волн высокого порядка к нестационарным задачам с использованием метода прямых. Требуется переформулировать дискретный закон сохранения как задачу оптимизации с ограниченями для дискретного решения и сетки, целью которой является выравнивание грани элемента с разрывами на каждом этапе Рунге-Кетты для каждого временного шага

    Сформулируем задачу отслеживания разрывов на заданном этапе i и шаге по времени n как задачу оптимизации с ограничениями, которая оптимизирует целевую функцию $f_{n,i}$

    То есть $\bold{u_{n,i}} \in \mathbb{R}^{N_u}$ и $\bold{x}_{n,i} \in \mathbb{R}^{N_x}$ как

    $(\bold{u}_{n,i},\bold{x}_{n,i}) := argmin \hskip{.2cm} f_{n,i}(\bold(w,y)) \hskip{.2cm}$ при условии $\bold{r}_{n,i}(\bold{(w,y)) \bold{ = 0}} \hskip{2cm} (43)$

    Для фиксированного временного шага n, как только вычислены состояния этапа {$\bold{u}_{n,i}$}$_{i=1}^s$ и сетки {$\bold{x}_{n,i}$}$_{i=1}^s$, состояние и сетка могут быть переведены на следующий временной шаг $(\bold{u}_{n+1},\bold{x}_{n+1})$ РК

    Неявные диаональные схемы Рунге-Кутта (DIRK) удовлетворяют свойству, что $A_{si} = b_i$ для $i = 1,\dots,s$ что подразумевает, что состояние и сетка на конечном этапе временного шага n идентичны состоянию и сетке на временной шаге n + 1, т.е. $\bold{u}_{n+1} = \bold{u}_{n,s}$ и $\bold{x}_{n+1} = \bold{x}_{n,s}$

    Целевая функция построена таким образом, что решением задачи оптимизации с ограниченями является сетка, выровненная по признакам, с использованием нормы оптимизированного остатка DG-DIRK

    $f_{n,i} : (\bold{w},\bold{y}) \mapsto \dfrac{1}{2} || \bold{R}_{n,i}(\bold{w},\bold{y})||^2_2$

    Эта же целевая функция использовалась для устойчивых законов сохранения, где было показано что она приводит к надежной системе отслеживания. В отличие от стационарного случая, мера качества сетки не включается в целевую функцию для нестационарного случая (метод прямых)

    В стационарном случае априори отсутсвует информация о местоположении волны, что обычно требует значительной деформации исходной сетки для выравниваня с волной, что требуется использования члена регуляризации сетки в целевой функции. Однако в контексте временного шага у нас есть полезная информация из предыдущего временного шага, которую можно использовать в качестве первоначального предположения как для состояния, так и для сетки. Эту информацию можно объединить вместе с условиями Рэнкина-Гюгонио и процедурой сглаживания сетки высокого порядка, чтобы получить отличное начальное предположение для сетки на каждом этапе Рунге-Кутты. В некотором смысле, дополнительное временное измерение позволяет отделить регуляризацию сетки от процедуры неявного отслеживания ударных волн, что является одним из приемуществ метода дискретизации линий по сравнению с пространственно-временной формулировкой нестационарных задач.
    ''')
    
if menu == 'SQP решатель':

    st.markdown(r'''
    ### SQP решатель

    Лагранжиан задачи оптимизации $\Im: \mathbb{R}^{N_u} \times \mathbb{R}^{N_x} \times \mathbb{R}^{N_u} \to \mathbb{R}$ принимает вид

    $$\Im (\bold{u,x,\lambda}) = f(\bold{u,x}) - \bold{\lambda}^T \bold{r}({\bold{u,x}})$$
    где $\bold{\lambda} \in \mathbb{R}^{N_u} $ - вектор множителей Лагранжа, связанных с ограничением DG. 

    Условия оптимальности первого порядка, или условия Каруша-Куна-Такера (KKT), утверждают, что $(\bold{u^*},\bold{x^*})$ является решением задачи оптимизации первого порядка, если существует $\bold{λ^⋆}$ такое, что:

    $$\dfrac{\partial f}{\partial u} (\bold{u^*},\bold{x^*})^T - \dfrac{\partial r}{\partial u}(\bold{u^*},\bold{x^*})^T \bold{\lambda^*} = 0 $$

    $$\dfrac{\partial f}{\partial x} (\bold{u^*},\bold{x^*})^T - \dfrac{\partial r}{\partial x}(\bold{u^*},\bold{x^*})^T \bold{\lambda^*} = 0 \hskip{2cm} \bold{r}(\bold{u^*},\bold{x^*})= \bold{0}$$

    Поскольку предполагается, что детерминант матрицы Якоби обратим относительно переменных состояния $\bold{u}$, мы определяем оценку оптимального множителя Лагранжа $\hat{λ} : \mathbb{R}^{N_u} \times \mathbb{R}^{N_x} \to \mathbb{R}^{N_u}$ таким образом, что первое уравнение $( \nabla_\bold{u} \Im = 0 )$ (сопряженное уравнение) всегда выполняется

    $\bold{\hat{\lambda}}(\bold{u},\bold{x}) = \dfrac{\partial r}{\partial u}(\bold{u},\bold{x})^{-T} \dfrac{\partial f}{\partial u} (\bold{u},\bold{x})^T$

    Тогда критерий оптимальности становится

    $\bold{c}(\bold{u^*},\bold{x^*}) :=\dfrac{\partial f}{\partial x} (\bold{u^*},\bold{x^*})^T - \dfrac{\partial r}{\partial x}(\bold{u^*},\bold{x^*})^T \dfrac{\partial r^*}{\partial u^*}(\bold{u^*},\bold{x^*})^{-T} \dfrac{\partial f}{\partial u} (\bold{u^*},\bold{x^*})^T = 0 \hskip{.5cm}$ $\bold{r}(\bold{u^*},\bold{x^*}) = 0$

    $\bold{u}^{k+1} = \bold{u}^k + \alpha_{k+1}\Delta\bold{u}^{k+1}, \hskip{3cm} \bold{x}^{k+1} = \bold{x}^k + \alpha_{k+1}\Delta\bold{x}^{k+1}$

    для $k=0,1,\dots,$ где $\alpha_{k+1} \in (0,1]$ - длина шага, который может быть определен процедурой линейного поиска, а $\bold{u}^{k+1}$ и $\bold{x}^{k+1}$ - направления поиска. На заднной итерации $k$ направления поиска $\bold{u}^{k}$ и $\bold{x}^{k}$ вычисляются одновременно как решение квадратичного подхода к задаче оптимизации с регуляризованной аппроксимацией Гессиана Левенберга-Марквардта.

    Пара $(\bold{u},\bold{x})$ является решением, если 
    
    $||\bold{c}(\bold{u,x})|| < \epsilon_1$ и $||\bold{r}(\bold{u,x})||<\epsilon_2, \hskip{2cm} \epsilon_1,\epsilon_2 > 0$
    ''')
