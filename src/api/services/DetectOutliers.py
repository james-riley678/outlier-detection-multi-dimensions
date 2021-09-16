# MyPy for Static Typing
from typing import List, Set, Dict, Tuple, Optional, Any, Union

# Customer Modules
from api.helpers.logger import logger

# PyPi Modules
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.metrics import mean_absolute_error
from os.path import splitext
from pandas.core.frame import DataFrame
from numpy import ndarray
import datetime

class DetectOutliers:
    def __init__(self) -> None:
        self = self

    def execute(self, fileName: str) -> str:
        extension: str = splitext(fileName)[1]
        df: DataFrame

        if extension == '.csv':
            df = pd.read_csv(f'files/{fileName}', header = None)
        elif extension == '.xlsx':
            df = pd.read_excel(f'files/{fileName}', header = None)
        else:
            raise DetectOutliersError(f'File type is {extension}, can only be of type: xlsx, csv')
        

        xTrain, xTest, yTrain, yTest = self.__splitData(df)

        results: List[dict] = []
        results.append(self.__isolationForest(xTrain, xTest, yTrain, yTest))
        results.append(self.__ellipticEnvelope(xTrain, xTest, yTrain, yTest))
        results.append(self.__localOutlierFactor(xTrain, xTest, yTrain, yTest))
        results.append(self.__oneClassSVM(xTrain, xTest, yTrain, yTest))

        resDf: DataFrame = pd.DataFrame(results)
        yhat: list = resDf[(resDf['r2'] == resDf['r2'].max())]['yhat'].values[0]
        bestR2: list = resDf[(resDf['r2'] == resDf['r2'].max())]['r2'].values[0]
        logger.info(f'Best R2: {bestR2}')
        df['yhat'] = yhat

        thisDateTime: str = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        newFileLocation: str = f'files/outliers_{thisDateTime}.csv'
        df.to_csv(newFileLocation, header = False, index=False)

        return newFileLocation
        
    def __isolationForest(self, xTrain, xTest, yTrain, yTest):
        logger.info('Isolation Forest')
        results: list = []
        iso: IsolationForest
        for i in range(1,50, 1):
            i = i / 100
            iso = IsolationForest(contamination=i)
            yhat = iso.fit_predict(xTrain)
            mask = yhat != -1
            results.append(dict(
                contamination = i,
                r2 = self.__getFit(xTrain[mask, :], xTest, yTrain[mask], yTest)
            ))
        resDf: DataFrame = pd.DataFrame(data = results)
        chosenContaminationValue: int = resDf[(resDf['r2'] == resDf['r2'].max())]['contamination'].values[0]
        bestR2: int = resDf[(resDf['r2'] == resDf['r2'].max())]['r2'].values[0]

        iso = IsolationForest(contamination=chosenContaminationValue)
        yhat = iso.fit_predict(self.x)
        
        resDict: dict = dict(r2 = bestR2, yhat = yhat)
        logger.debug(resDict)
        return resDict

    def __ellipticEnvelope(self, xTrain, xTest, yTrain, yTest):
        logger.info('Eliptic Envelope')
        results: list = []
        ee: EllipticEnvelope
        for i in range(1,50, 1):
            i = i / 100
            ee = EllipticEnvelope(contamination=i)
            yhat = ee.fit_predict(xTrain)
            mask = yhat != -1
            results.append(dict(
                contamination = i,
                r2 = self.__getFit(xTrain[mask, :], xTest, yTrain[mask], yTest)
            ))
        resDf: DataFrame = pd.DataFrame(data = results)
        chosenContaminationValue: int = resDf[(resDf['r2'] == resDf['r2'].max())]['contamination'].values[0]
        bestR2: int = resDf[(resDf['r2'] == resDf['r2'].max())]['r2'].values[0]

        ee = EllipticEnvelope(contamination=chosenContaminationValue)
        yhat = ee.fit_predict(self.x)
        return  dict(r2 = bestR2, yhat = yhat)

    def __localOutlierFactor(self, xTrain, xTest, yTrain, yTest):
        logger.info('Local Outlier Factor')
        results: list = []
        lof: LocalOutlierFactor
        for i in range(1,50, 1):
            i = i / 100
            lof = LocalOutlierFactor(contamination = i)
            yhat = lof.fit_predict(xTrain)
            mask = yhat != -1
            results.append(dict(
                contamination = i,
                r2 = self.__getFit(xTrain[mask, :], xTest, yTrain[mask], yTest)
            ))
        resDf: DataFrame = pd.DataFrame(data = results)
        chosenContaminationValue: int = resDf[(resDf['r2'] == resDf['r2'].max())]['contamination'].values[0]
        bestR2: int = resDf[(resDf['r2'] == resDf['r2'].max())]['r2'].values[0]
        lof = LocalOutlierFactor(contamination=chosenContaminationValue)
        yhat = lof.fit_predict(self.x)
        return  dict(r2 = bestR2, yhat = yhat)

    def __oneClassSVM(self, xTrain, xTest, yTrain, yTest):
        logger.info('One Class SVM')
        results: list = []
        ee: OneClassSVM
        for i in range(1,50, 1):
            i = i / 100
            ee = OneClassSVM(nu=i)
            yhat = ee.fit_predict(xTrain)
            mask = yhat != -1
            results.append(dict(
                nu = i,
                r2 = self.__getFit(xTrain[mask, :], xTest, yTrain[mask], yTest)
            ))
        resDf: DataFrame = pd.DataFrame(data = results)
        chosenNuValue: int = resDf[(resDf['r2'] == resDf['r2'].max())]['nu'].values[0]
        bestR2: int = resDf[(resDf['r2'] == resDf['r2'].max())]['r2'].values[0]

        ee = OneClassSVM(nu=chosenNuValue)
        yhat = ee.fit_predict(self.x)
        return  dict(r2 = bestR2, yhat = yhat)

    def __getFit(self, xTrain, xTest, yTrain, yTest):
        model = LinearRegression(fit_intercept= True, normalize=False)
        model.fit(xTrain, yTrain)
        rSquared = model.score(xTest, yTest)
        logger.debug(f'R2: {rSquared}')

        return rSquared

    def __splitData(self, df: DataFrame):
        data: list = df.values

        self.x: ndarray; self.y: ndarray; testSize: int 
        self.x, self.y = data[:, :-1], data[:, -1]
        if self.x.shape[0] >= 1000:
            testSize = 0.2
        else:
            testSize = 0.33
        xTrain, xTest, yTrain, yTest = train_test_split(self.x, self.y, test_size=testSize, random_state=10)
        return xTrain, xTest, yTrain, yTest

class DetectOutliersError(Exception):
    pass